from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView

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
            grp_name = form.cleaned_data['grp_name']
            schedule_cadence(cadence, grp_name, datetime)
            messages.info(request, 'Cadence Executed')
        return redirect(reverse_lazy('cadence:cadence-list'))

    return render(request, 'cadence/cadence-execute.html', context)
