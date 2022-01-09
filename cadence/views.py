from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView
from message_scripts.models import MessageScript
from message_scripts import forms as script_form
from scripts.backgroundprocess import schedule_cadence
from . import forms, models


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
