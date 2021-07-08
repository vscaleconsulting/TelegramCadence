from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, DeleteView

from . import forms, models


class MessageScriptUpdateView(UpdateView):
    template_name = 'message_scripts/message-update.html'
    model = models.MessageScript
    form_class = forms.MessageScriptModelForm

    def get_success_url(self):
        return reverse_lazy('cadence:cadence-detail', kwargs={'pk': self.kwargs['c_pk']})


class MessageScriptDeleteView(DeleteView):
    template_name = 'message_scripts/message-delete.html'
    model = models.MessageScript

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['c_pk'] = self.kwargs['c_pk']
        return context

    def get_success_url(self):
        messages.info(self.request, 'Deleted')
        return reverse('cadence:cadence-detail', kwargs={'pk': self.kwargs['c_pk']})
