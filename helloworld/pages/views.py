from django import forms
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.
class HomePageView(TemplateView):
    template_name = "pages/home.html"

class AboutPageView(TemplateView): 
    template_name = 'pages/about.html' 
 
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context.update({ 
            "title": "About us - Online Store", 
            "subtitle": "About us", 
            "description": "This is an about page ...", 
            "author": "Developed by: Samuel Herrera Hoyos", 
        }) 
 
        return context
    
class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context.update({ 
            "email": "pruebaemail@eafit.edu.co", 
            "subtitle": "Contact us", 
            "address": "CARRERA 49 7 SUR 50, MEDEllIN, ANTIOQUIA", 
            "phoneNumber": "6042619500", 
        }) 
 
        return context 
    
class Product:
    products = [
        {"id": "1", "name": "TV", "description": "Best TV", "price": 120},
        {"id": "2", "name": "iPhone", "description": "Best iPhone", "price": 999},
        {"id": "3", "name": "Chromecast", "description": "Best Chromecast", "price": 80},
        {"id": "4", "name": "Glasses", "description": "Best Glasses", "price": 30},
    ]

class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self,request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of Products"
        viewData["products"] = Product.products

        return render(request, self.template_name, viewData)


class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        if not id.isdigit() or int(id) < 1 or int(id) > len(Product.products):
            return HttpResponseRedirect(reverse('home'))

        viewData = {}
        product = Product.products[int(id)-1]
        viewData["title"] = product["name"] + " - Online Store"
        viewData["subtitle"] = product["name"] + " - Product information"
        viewData["product"] = product
        return render(request, self.template_name, viewData)

class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductForm()
        viewData = {
            "title": "Create product",
            "form": form
        }
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            return render(request, 'products/product_created.html', {'title': 'Product created'})
        return render(request, self.template_name, {'form': form, 'title': 'Create product'})
