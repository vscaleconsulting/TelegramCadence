import asyncio

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, ListView, DetailView
from telethon.sessions import StringSession
from telethon.sync import TelegramClient

from . import models

clients = {}


class TgAccountCreateView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'accounts/account-create.html')

    def post(self, *args, **kwargs):
        if self.request.POST.get('phoneNum'):
            # return render(self.request, 'accounts/account-otp.html', {'phone_num': self.request.POST.get('phoneNum')})
            return redirect(
                reverse_lazy('accounts:account-otp', kwargs={'phone_num': self.request.POST.get('phoneNum')}))
        return render(self.request, 'accounts/account-create.html')


def get_otp(request, phone_num):
    global clients

    if request.method == 'POST':
        otp = request.POST.get('otp')
        client = clients[phone_num]
        clients.pop(phone_num)

        client.connect()
        pch = request.session.get('pch')

        client.sign_in(phone_num, otp, phone_code_hash=pch)
        session_str = client.session.save()
        user = client.get_me()
        client.disconnect()
        models.Account.objects.create(user=request.user,
                                      acc_name=user.first_name + (
                                          '' if user.last_name is None else f' {user.last_name}'),
                                      acc_username=user.username,
                                      acc_id=user.id,
                                      sess_str=session_str,
                                      phone=int(user.phone))
        return redirect(reverse_lazy('core:home-page'))

    api_id = 1868530
    api_key = "edf7d1e794e0b4a5596aa27c29d17eba"
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    client = TelegramClient(StringSession(), api_id, api_key, loop=loop)
    client.connect()

    code = client.send_code_request(phone_num)
    client.disconnect()
    request.session['pch'] = code.phone_code_hash
    clients[phone_num] = client
    return render(request, 'accounts/account-otp.html')


#
class TgAccountDeleteView(DeleteView):
    template_name = 'accounts/account-delete.html'
    model = models.Account
    context_object_name = 'account'
    success_url = reverse_lazy('account:account-list')


class TgAccountListView(ListView):
    template_name = 'accounts/account-list.html'
    model = models.Account

    context_object_name = 'account'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TgAccountDetailView(DetailView):
    template_name = 'accounts/account-detail.html'
    context_object_name = 'account'

    model = models.Account

# def get_queryset(self):
#     account = models.Account.objects.get(pk=self.kwargs['pk'])
#     return account.group_set.all()
