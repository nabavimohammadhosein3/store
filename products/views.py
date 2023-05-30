import random

from django.views import View
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, StreamingHttpResponse
from django.template import loader
from django.views.generic import FormView, View
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response, SimpleTemplateResponse
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
import jwt
import requests

from .models import Producte, Category, Comment, Buy
from accounts.models import Account

def my_auth(request):
    jwt_token = request.COOKIES.get('jwt-access')

    if jwt_token:
        decode_token = jwt.decode(jwt_token, settings.SECRET_KEY, ['HS256'])
        if Account.objects.get(id= decode_token['user_id']):
            return decode_token['user_id']
    else:
        return 'redire'

class HomeView(APIView):
    
    def get(self, request):
        result = my_auth(request)
        template = loader.get_template('products/home.html')
        context = {'category': Category.objects.all(), 'product': Producte.objects.order_by('off')}
        if result != 'redire':
            context = {'category': Category.objects.all(), 'product': Producte.objects.order_by('off'), 'account': Account.objects.get(id= result)}
        return HttpResponse(content=template.render(context, request))
        
class ProductView(View):
    def get(self, request, pk):
        result = my_auth(request)
        template = loader.get_template('products/product.html')
        context = {'product': Producte.objects.get(pk=pk)}
        if result != 'redire':
            context = {'product': Producte.objects.get(pk=pk), 'account': Account.objects.get(id= result), 
                       'buy': Buy.objects.filter(user = Account.objects.get(id= result), is_purchase = False, product = Producte.objects.get(pk=pk))}
        return HttpResponse(content=template.render(context, request))

class BuyView(View):

    def post(self, request, pk):
        result = my_auth(request)
        if result != 'redire':
            Buy.objects.create(user=Account.objects.get(id= result), is_purchase=False, product=Producte.objects.get(id=request.POST.get('id')))
            return JsonResponse({})
        else:
            return JsonResponse({'error': 'login'})

    def put(self, request, pk):
        result = my_auth(request)
        if result != 'redire':
            buy = Buy.objects.filter(user= Account.objects.get(id= result), is_purchase = False)
            for b in buy:
                p = b.product
                p.count -= 1
                p.save()
                if p.count == 0:
                    p.delete()
            buy.update(is_purchase = True)
            return JsonResponse({})
        else:
            return JsonResponse({'error': 'login'})
        
    def delete(self, request, pk):
        result = my_auth(request)
        if result != 'redire':
            buy = Buy.objects.get(id=pk).delete()
            return JsonResponse({})
        else:
            return JsonResponse({'error': 'login'})
        
class CommentView(View):

    def post(self, request, pk):
        result = my_auth(request)
        if result != 'redire':
            if request.POST.get('text').strip() != '':
                Comment.objects.create(user=Account.objects.get(id= result), describtion= request.POST.get('text'), 
                                    producte=Producte.objects.get(id=request.POST.get('id')))
                return JsonResponse({'error': 'correct'})
            else:
                return JsonResponse({'error': 'empty'})
        else:
            return JsonResponse({'error': 'login'})
        
    def delete(self, request, pk):
        result = my_auth(request)
        if result != 'redire':
            Comment.objects.get(id=pk).delete()
            return JsonResponse({})
        else:
            return JsonResponse({'error': 'login'})

class CategoryView(View):
    
    def get(self, request, title):
        result = my_auth(request)
        template = loader.get_template('products/category.html')
        context = {'title': title, 'category': Category.objects.all(), 'product': Producte.objects.order_by('off')}
        if result != 'redire':
            context = {'title': title, 'category': Category.objects.all(), 'product': Producte.objects.order_by('off'), 'account': Account.objects.get(id= result)}
        return HttpResponse(content=template.render(context, request))
    
class SearchView(View):
    
    def get(self, request):
        result = my_auth(request)
        template = loader.get_template('products/search.html')
        search = request.GET['search']
        context = {'search': search, 'product': Producte.objects.filter(Q(title__icontains=search) | Q(category__title__icontains=search))}
        if result != 'redire':
            context = {'search': search, 'product': Producte.objects.filter(Q(title__icontains=search) | Q(category__title__icontains=search)), 'account': Account.objects.get(id= result)}
        return HttpResponse(content=template.render(context, request))