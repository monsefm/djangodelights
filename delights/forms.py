from django import forms
from .models import Inventory, MenuItem, Customer, Purchase, RecipeRequirement

#Ingredient forms
class InventoryCreateForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ('ingredient', 'price', 'stock', 'create_by')


class InventoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ('ingredient', 'price', 'stock', 'create_by')


#Menu forms
class MenuCreateForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ('menu_type', 'name', 'handwork_price', 'create_by')


class MenuUpdateForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ('menu_type','name', 'handwork_price', 'create_by')


#Recipe forms
class RecipeCreateForm(forms.ModelForm):
    class Meta:
        model = RecipeRequirement
        fields = ('inventory_id', 'menuitem_id', 'cant')


class RecipeUpdateForm(forms.ModelForm):
    class Meta:
        model = RecipeRequirement
        fields = ('inventory_id','menuitem_id', 'cant')



#Customer forms
class CustomerCreateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name')


class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('first_name','last_name')



#Purchase forms
class PurchaseCreateForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ('customer_id', 'menuitem_id', 'day' ,'time')
    
    def __init__(self, user=None, **kwargs):
        super(PurchaseCreateForm, self).__init__(**kwargs)      

        menu_ids = [m.id for m in MenuItem.objects.all() if m.have_stock() == 'available' ] 
        self.fields['menuitem_id'].queryset = MenuItem.objects.filter(id__in=menu_ids).order_by('name')

class PurchaseUpdateForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ('customer_id', 'menuitem_id', 'day' ,'time')
    
    def __init__(self, user=None, **kwargs):
        super(PurchaseUpdateForm, self).__init__(**kwargs)   
        menu_ids = [m.id for m in MenuItem.objects.all() if not m.have_stock() == 'no recipe'  ] 
        self.fields['menuitem_id'].queryset = MenuItem.objects.filter(id__in=menu_ids).order_by('name') 


