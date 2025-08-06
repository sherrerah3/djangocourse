from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.core.exceptions import ValidationError
from .models import Product


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
    
class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self,request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of Products"
        viewData["products"] = Product.objects.all()

        return render(request, self.template_name, viewData)


class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        # Check if product id is valid
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Product id must be 1 or greater")
            product = get_object_or_404(Product, pk=product_id)
        except (ValueError, IndexError):
            # If the product id is not valid, redirect to the home page
            return HttpResponseRedirect(reverse('home'))

        viewData = {}
        product = get_object_or_404(Product, pk=product_id)
        viewData["title"] = product.name + " - Online Store"
        viewData["subtitle"] = product.name + " - Product information"
        viewData["product"] = product
        return render(request, self.template_name, viewData)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','price']

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
            form.save()
            return redirect('/products/create')
        else:
            viewData = {}
            viewData['title'] = "Create Product"
            viewData['form'] = form
            return render(request, self.template_name, viewData)


class ProductListView(ListView):
    model = Product
    template_name = 'products_list.html'
    context_object_name = 'products' # This will allow u to loop through 'products' in your template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Products - Online Store'
        context['subtitle'] = 'List of Products'
        return context
    