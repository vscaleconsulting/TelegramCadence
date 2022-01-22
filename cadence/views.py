from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView
from message_scripts.models import MessageScript
from message_scripts import forms as script_form
from scripts.backgroundprocess import schedule_cadence
from . import forms, models
from . import validators
from scripts.functions import fetch_messages_gspread
from accounts.models import Account
from cadence.functions import create_mass_messages

class CadenceCreateView(CreateView):
    template_name = 'cadence/cadence-create.html'
    form_class = forms.CadenceModelForm

    def form_valid(self, form):
        cadence = form.save(commit=False)
        cadence.user = self.request.user
        cadence.save()

        return super().form_valid(form)

    success_url = reverse_lazy('cadence:cadence-list')


class CadenceDeleteView(DeleteView):
    template_name = 'cadence/cadence-delete.html'
    model = models.Cadence
    context_object_name = 'cadence'
    success_url = reverse_lazy('cadence:cadence-list')


class CadenceListView(ListView):
    template_name = 'cadence/cadence-list.html'
    model = models.Cadence

    context_object_name = 'cadence'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


def cadence_detail(request, pk):
    cadence = models.Cadence.objects.get(pk=pk)
    messages_script = cadence.messagescript_set.all()
    form = script_form.MessageScriptModelForm()

    context = {
        'pk': pk,
        'form': form,
        'messages_scripts': messages_script
    }

    if request.method == 'POST':
        form = script_form.MessageScriptModelForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.cadence = cadence
            form.user = request.user    
            form.save()

    return render(request, 'cadence/cadence-detail.html', context)

def duplicated_cadence(request,pk):
    cadence = models.Cadence.objects.get(pk=pk)
    messages_script = cadence.messagescript_set.all()
    
    
    duplicate_cadence = models.Cadence.objects.create(user=cadence.user,name=f"{cadence.name}_duplicated")
    for message_script in messages_script:
        cadence_ = duplicate_cadence
        account = message_script.account
        message = message_script.message
        time_days = message_script.time_days
        time_hours = message_script.time_hours
        time_minutes = message_script.time_minutes
        time_seconds = message_script.time_seconds

        MessageScript.objects.create(cadence=cadence_,account=account,message=message,time_days=time_days,time_hours=time_hours,time_minutes=time_minutes,time_seconds=time_seconds)
        

    return redirect("cadence:cadence-list")
    
def cadence_execute(request, pk):
    cadence = models.Cadence.objects.get(pk=pk)
    form = forms.ExecuteCadenceForm()
    
    context = {
        'form': form,
        'pk': pk
    }
    if request.method == 'POST':
        form = forms.ExecuteCadenceForm(request.POST)
        if form.is_valid():
            datetime = form.cleaned_data['global_time']
            grps_name = form.cleaned_data['grp_name'].split(",")
            
            for groups in grps_name:
                schedule_cadence(cadence, groups, datetime)
                
            messages.info(request, 'Cadence Executed')
        return redirect(reverse_lazy('cadence:cadence-list'))

    return render(request, 'cadence/cadence-execute.html', context)


def cadence_import(request,pk):

    cadence = models.Cadence.objects.get(pk=pk)
    messages_scripts = MessageScript.objects.all().filter(cadence=cadence)
    accounts = Account.objects.all().filter(user=request.user)

    if request.method=="POST":
        url = request.POST["url"]
        sheet_no = int(request.POST["sheet_no"])
        names_col = int(request.POST["names_col"])
        messages_col = int(request.POST["messages_col"])
        starting_row = int(request.POST["starting_row"])
        ending_row = int(request.POST["ending_row"])
        days = int(request.POST["days"])
        hours =  int(request.POST["hours"])
        minutes =  int(request.POST["minutes"])
        seconds =  int(request.POST["seconds"])
        

        #  validation check
        args = [sheet_no,names_col,messages_col,starting_row,ending_row,days,hours,minutes,seconds]
        validators.cadence_import_args_validator(request, url, args)

        # fetch messages from url : starting_row to ending_row -> int
        try:
            names,messages_list = fetch_messages_gspread(url,sheet_no,starting_row,ending_row,names_col,messages_col)
        except Exception as e:
            print("error log",e)
            messages.error(request, f"{e}")
            return redirect("cadence:cadence-detail",pk)

        # create message_scripts from messages and accounts
        create_mass_messages(names,messages_list,cadence,days,hours,minutes,seconds)
        messages.info(request,"imported messages")
        

    context = {
        "cadence_name":cadence.name,
        "messages_scripts":messages_scripts,
        "pk":pk,
        "accounts":accounts
    }


    return render(request,"cadence/cadence-import.html",context)