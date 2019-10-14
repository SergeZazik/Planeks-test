from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tasks import user_email_activate_task

from .forms import CustomUserCreateForm
from .token_generator import account_activation_token
from .models import CustomUser


class SignUpView(CreateView):
    """
    Registration view
    """
    form_class = CustomUserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    success_message = 'Account was successfully created!'

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.is_active = False
            user.save()

            current_site = get_current_site(self.request)
            mail_subject = 'Please Activate Your Account.'
            message = render_to_string('activate_account_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')

            user_email_activate_task.delay(mail_subject, message, to_email)

            return render(self.request, 'activate_account.html')
        return self.form_valid(form)


def activate_account(request, uidb64, token):
    """
    View that allows to activate new account via email
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'activate_account_success.html')
    else:
        return HttpResponse('Activation link is invalid!')
