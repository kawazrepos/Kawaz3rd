# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/13
#
from django.template.loader import render_to_string
from django.views.generic import simple
from django.contrib import messages
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect

from django.views.generic.edit import FormView
from django.db.models import Q
from kawaz.core.personas.models import Persona
from .forms import EmailForm

class ContactFormView(FormView):
    template_name = 'contacts/contact_form.html'
    form_class = EmailForm

    def form_valid(self, form):
        is_staff = Q(role='seele') || Q(role='nerv') || Q(role='adam')
        admin_list = Persona.objects.filter(is_staff)
        try:
            site = Site.objects.get_current()
            ctx_dict = {
                'site': site,
                'sender': form.cleaned_data['sender'],
                'subject': form.cleaned_data['subject'],
                'body': form.cleaned_data['body']
            }
            subject = render_to_string('contact/email_subject.txt', ctx_dict)
            subject = ''.join(subject.splitlines())
            body = render_to_string('contact/email.txt', ctx_dict)
            recivers = admin_list.exclude(email='')
            for reciver in recivers:
                reciver.email_user(subject, body, from_email=form.cleaned_data['sender'])
            return HttpResponseRedirect(self.get_success_url())
        except:
            return self.form_invalid()

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

def email(request):
    # 管理者グループの指定(ネルフ)
    admin_group = Group.objects.get(name='nerv')
    admin_list = admin_group.user_set.filter(is_active=True).exclude(profile__nickname=None)
    if request.method == 'POST':
        form = EmailForm(request.POST)
        try:
            form.is_valid()
            site = Site.objects.get_current()
            ctx_dict = {
                'site': site,
                'sender': form.cleaned_data['sender'],
                'subject': form.cleaned_data['subject'],
                'body': form.cleaned_data['body']
            }
            subject = render_to_string('contact/email_subject.txt', ctx_dict)
            subject = ''.join(subject.splitlines())
            body = render_to_string('contact/email.txt', ctx_dict)
            recivers = admin_list.exclude(email='')
            for reciver in recivers:
                reciver.email_user(subject, body, from_email=form.cleaned_data['sender'])
            message = u"メールを送信しました"
            messages.success(request, message, fail_silently=True)
        except ValidationError as e:
            message = u"日本語が含まれていない文章は送信できません"
            messages.error(request, message)
        except:
            message = u"エラーが発生しました"
            messages.error(request, message)

    else:
        form = EmailForm()
    kwargs = {
        'template': r'contact/email_form.html',
        'extra_context': {
            'form': form,
            'admin_group': admin_group,
            'admin_list': admin_list,
        },
    }
    return simple.direct_to_template(request, **kwargs)