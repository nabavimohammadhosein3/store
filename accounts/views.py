import datetime
import requests
from django.conf import settings

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import loader
from django.views.generic import FormView, View
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from rest_framework.views import APIView
import jwt

from .forms import SignUpForm, AccountForm
from .models import Account
from products.models import Buy

def my_auth(request):

    jwt_token = request.COOKIES.get('jwt-access')

    if jwt_token:
        decode_token = jwt.decode(jwt_token, settings.SECRET_KEY, ['HS256'])
        if Account.objects.get(id= decode_token['user_id']):
            return decode_token['user_id']
    else:
        return 'redire'

class SignUpView(View):
    def get(self, request):
        result = my_auth(request)
        if result == 'redire':
            form = SignUpForm()
            template = loader.get_template('account/signup.html')
            context = {'form': form}
            return HttpResponse(content=template.render(context, request)) 
        else:
            return HttpResponseRedirect('/account/')
    
    def post(self, request):
        result = my_auth(request)
        if result == 'redire':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/account/login/')
            else:
                template = loader.get_template('account/signup.html')
                context = {'form': form}
                return HttpResponse(content=template.render(context, request)) 
        else:
            return HttpResponseRedirect('/account/')

class AccountView(View):

    def get(self, request):
        result = my_auth(request)
        if result != 'redire':
            template = loader.get_template('account/account.html')
            account = Account.objects.get(id= result)
            form = AccountForm(request.POST or None, instance=account, initial={'avatar': account.avatar.name})
            context = {'account': Account.objects.get(id= result), 
                       'buy': Buy.objects.filter(user= Account.objects.get(id= result)), 'form': form}
            return HttpResponse(content=template.render(context, request))
        else:
            return HttpResponseRedirect('/account/login/')
        
    def post(self, request):
        result = my_auth(request)
        if result != 'redire':
            template = loader.get_template('account/account.html')
            account = Account.objects.get(id= result)
            form = AccountForm(request.POST , request.FILES, instance=account, initial={'avatar': account.avatar.name})
            if form.is_valid():
                avatar = form.save(commit=False)
                avatar.avatar = request.FILES['avatar']
                avatar.save()
                return HttpResponseRedirect('/account/')
            else:
                context = {'account': Account.objects.get(id= result), 
                           'buy': Buy.objects.filter(user= Account.objects.get(id= result)), 'form': form}
                return HttpResponse(content=template.render(context, request))
        else:
            return HttpResponseRedirect('/account/login/')
        
class LoginView(View):

    def get(self, request):
        if my_auth(request) == 'redire':
            template = loader.get_template('account/login.html')
            return HttpResponse(content=template.render({}, request))
        else:
            return HttpResponseRedirect('/account/')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)

        if not user:
            return JsonResponse({'error': 'username or password is incorrect'})
        
        else:
            return JsonResponse({'error': 'correct'})