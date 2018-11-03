from django.shortcuts import render, redirect
from django.views import View
from .read_emails import get_emails

# Create your views here.
class HomeView(View):
    template_name = "index.html"

    def get(self, request, *arg, **kwargs):
         return render(request, self.template_name)

    def post(self, request, *arg, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email is not None and password is not None:
            context = {
                'email': email,
                'password': password
            }
            message_list, login_failed = get_emails(email, password)
            if login_failed:
                error_message = 'Invalid credentials'
                return render(request, self.template_name, {'error_message': error_message})
            return render(request, self.template_name, {'message_list': message_list})
        context = {
            'message': 'enter email or password'
        }
        return render(request, self.template_name, {'context': context})
