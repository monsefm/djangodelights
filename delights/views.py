from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import UserCreationForm
from .models import Inventory, MenuItem, RecipeRequirement, Customer, Purchase
from .forms import InventoryCreateForm, InventoryUpdateForm, MenuCreateForm, MenuUpdateForm, RecipeCreateForm, RecipeUpdateForm, CustomerCreateForm, CustomerUpdateForm, PurchaseCreateForm, PurchaseUpdateForm


# Create your views here.
@login_required
def home(request):
    context = {'user': request.user}
    return render(request, 'delights/home.html', context)


@login_required
def get_recipes(request, menuid):
   menu_info = MenuItem.objects.get(pk=menuid)
   reqrecipes = RecipeRequirement.objects.filter(menuitem_id=menuid)
 
   recipes = []
   recipes = [{'id': r.id, 'inventory_id': r.inventory_id, 'menuitem_id': r.menuitem_id, 'menuitem_name': r.menuitem_id.name, 'cant': r.cant, 'ingredient_name':r.inventory_id.ingredient} for r in reqrecipes]
 
   context = {'recipes': recipes, 'menuid':menuid, 'menu_name': menu_info.name}
   return render(request, 'delights/reciperequirement_list.html', context)


@login_required
def get_purchases_customer(request, customerid):
   customer_info = Customer.objects.get(pk=customerid)
   purchase_set = Purchase.objects.filter(customer_id=customerid) 
   purchases = list()
   total = 0

   for p in purchase_set:
      purchases.append({'id': p.id, 'customer_id': p.customer_id, 'menuitem_id': p.menuitem_id, 'menuitem_name': p.menuitem_id.name, 'day': p.day, 'time':p.time ,'total':  p.menuitem_id.price} )    
      total = total + p.menuitem_id.price
 
   context = {'purchases': purchases, 'customerid':customerid, 'customer_name': customer_info, 'total':total }
   return render(request, 'delights/purchase_list_customer.html', context)


@login_required
def get_purchases(request):
   search = request.GET.get("search", None)
   
   purchase_set = Purchase.objects.all()
   purchases = list()
   total = 0

   if search:     
      purchase_set = purchase_set.filter(day=search)

   for p in purchase_set:
      purchases.append({'id': p.id, 'customer_id': p.customer_id, 'menuitem_id': p.menuitem_id, 'menuitem_name': p.menuitem_id.name, 'day': p.day, 'time':p.time ,'total':  p.menuitem_id.price} )    
      total = total + p.menuitem_id.price
 
   context = {'purchase_list': purchases, 'total':total }
   return render(request, 'delights/purchase_list.html', context)


@login_required
def get_inventary(request):
   inventary_set = Inventory.objects.all()
   inventary = list()
   total = 0
  
   for i in inventary_set:
      i.re_stock()
      inventary.append({'id': i.id, 'ingredient':i.ingredient, 'price':i.price, 'stock': i.stock, 'create_by': i.create_by, 're_stock': i.used_stock, 'current_stock': (i.stock - i.used_stock)})
      total = total + (i.stock*i.price)
   
   context = {'inventory_list': inventary, 'total':total}
   return render(request, 'delights/inventory_list.html', context)


@login_required
def get_logout(request):
    logout(request)
    return redirect('home')


#INVENTORY
class InventoryList(LoginRequiredMixin, ListView):
   model = Inventory

class InventoryCreate(LoginRequiredMixin, CreateView):
   model = Inventory
   template_name = 'delights/inventory_create.html'
   form_class = InventoryCreateForm

   def get_context_data(self, **kwargs):
      kwargs = super(InventoryCreate, self).get_context_data(**kwargs)        
    
      kwargs['form'] = InventoryCreateForm(
        initial={
        'create_by': self.request.user    
      })
      return kwargs

class InventoryUpdate(LoginRequiredMixin, UpdateView):
   model = Inventory
   template_name = 'delights/inventory_update.html'
   form_class = InventoryUpdateForm

class InventoryDelete(LoginRequiredMixin, DeleteView):
    model = Inventory
    template_name = 'delights/inventory_delete.html'
    success_url = '/inventory/list'



#MENUITEM
class MenuItemList(LoginRequiredMixin, ListView):
   model = MenuItem

class MenuItemCreate(LoginRequiredMixin, CreateView):
   model = MenuItem
   template_name = 'delights/menuitem_create.html'
   form_class = MenuCreateForm

   def get_context_data(self, **kwargs):
      kwargs = super(MenuItemCreate, self).get_context_data(**kwargs)        

      kwargs['form'] = MenuCreateForm(
        initial={
        'create_by': self.request.user    
      })
      return kwargs

class MenuItemUpdate(LoginRequiredMixin, UpdateView):
   model = MenuItem
   template_name = 'delights/menuitem_update.html'
   form_class = MenuUpdateForm

class MenuItemDelete(LoginRequiredMixin, DeleteView):
    model = MenuItem
    template_name = 'delights/menuitem_delete.html'
    success_url = '/menuitem/list'


#RECIPEREQUIREMENTS
class RecipeReqList(LoginRequiredMixin, ListView):
   model = RecipeRequirement
   
class RecipeReqCreate(LoginRequiredMixin, CreateView):
   model = RecipeRequirement
   template_name = 'delights/reciperequirement_create.html'
   form_class = RecipeCreateForm

   def get_context_data(self, **kwargs):
      kwargs = super(RecipeReqCreate, self).get_context_data(**kwargs)
      kwargs['menuid'] = self.kwargs.get('menuid')
      kwargs['form'] = RecipeCreateForm(
        initial={
        'menuitem_id': kwargs['menuid']     
      })
      return kwargs
   
   def get_success_url(self):   
      context =  self.get_context_data()       
      return reverse('recipereqlist', kwargs={'menuid': context['menuid']})


class RecipeReqUpdate(LoginRequiredMixin, UpdateView):
   model = RecipeRequirement
   template_name = 'delights/reciperequirement_update.html'
   form_class = RecipeUpdateForm
  

   def get_context_data(self, **kwargs):
      kwargs = super(RecipeReqUpdate, self).get_context_data(**kwargs)
      kwargs['menuid'] = self.kwargs.get('menuid')
      return kwargs
   
   def get_success_url(self):   
      context =  self.get_context_data()       
      return reverse('recipereqlist', kwargs={'menuid': context['menuid']})


class RecipeReqDelete(LoginRequiredMixin, DeleteView):
   model = RecipeRequirement
   template_name = 'delights/reciperequirement_delete.html'
   success_url = '/recipereq/list'

   def get_context_data(self, **kwargs):
      kwargs = super(RecipeReqDelete, self).get_context_data(**kwargs)
      kwargs['menuid'] = self.kwargs.get('menuid')
      return kwargs
   
   def get_success_url(self):   
      context =  self.get_context_data()       
      return reverse('recipereqlist', kwargs={'menuid': context['menuid']})



#CUSTOMER
class CustomerList(LoginRequiredMixin, ListView):
   model = Customer

class CustomerCreate(LoginRequiredMixin, CreateView):
   model = Customer
   template_name = 'delights/customer_create.html'
   form_class = CustomerCreateForm

   def get_context_data(self, **kwargs):
      kwargs = super(CustomerCreate, self).get_context_data(**kwargs)     
      kwargs['form'] = CustomerCreateForm(
        initial={
        'create_by': self.request.user    
      })
      return kwargs

class CustomerUpdate(LoginRequiredMixin, UpdateView):
   model = Customer
   template_name = 'delights/customer_update.html'
   form_class = CustomerUpdateForm

class CustomerDelete(LoginRequiredMixin, DeleteView):
    model = Customer
    template_name = 'delights/customer_delete.html'
    success_url = '/customer/list'



#PURCHASE
class PurchaseList(LoginRequiredMixin, ListView):
   model = Purchase   
   
class PurchaseCreate(LoginRequiredMixin, CreateView):
   model = Purchase
   template_name = 'delights/purchase_create.html'
   form_class = PurchaseCreateForm
   
   def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PurchaseUpdate(LoginRequiredMixin, UpdateView):
   model = Purchase
   template_name = 'delights/purchase_update.html'
   form_class = PurchaseUpdateForm
   
  

class PurchaseDelete(LoginRequiredMixin, DeleteView):
   model = Purchase
   template_name = 'delights/purchase_delete.html'
   success_url = '/purchase/list/'
   