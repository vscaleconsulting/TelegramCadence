from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, FormView

from message_scripts import forms as script_form
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


class CadenceDetailView(View):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass


def cadence_detail(request, pk):
    cadence = models.Cadence.objects.get(pk=pk)
    messages = cadence.messagescript_set.all()
    form = script_form.MessageScriptModelForm()

    context = {
        'form': form,
        'messages': messages
    }

    if request.method == 'POST':
        form = script_form.MessageScriptModelForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            form = form.save(commit=False)
            form.cadence = cadence
            form.user = request.user
            form.save()

    return render(request, 'cadence/cadence-detail.html', context)


# def get_queryset(self):
#     account = models.Account.objects.get(pk=self.kwargs['pk'])
#     return account.group_set.all()

def cadence_execute(request, pk):
    cadence = models.Cadence.objects.get(pk=pk)
    form = forms.ExecuteCadenceForm()
    
    context = {
        'form': form
    }
    
    return render(request, 'cadence/cadence-execute.html', context)

