from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count,Sum

# Create your models here.
class Inventory(models.Model):
    ingredient = models.CharField(max_length=50)
    price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    used_stock = models.IntegerField(default=0)
    create_by = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)

    def get_absolute_url(self):
        return '/inventory/list'

    def __str__(self):
        return f'{self.ingredient} ({self.stock}), ${self.price}'    

    def re_stock(self,*args, **kwargs):
        used_stock = 0
        if self.reciperequirement_set.count() > 0:
            recipes = RecipeRequirement.objects.filter(inventory_id = self.id)
            for r in recipes:
                if (r.menuitem_id).purchase_set.count() > 0:
                    used_stock = (used_stock + (r.cant)) * (r.menuitem_id).purchase_set.count()
        
        self.used_stock = used_stock
        super(Inventory, self).save(*args, **kwargs) 
        return used_stock 
                    
                


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)    

    def get_absolute_url(self):
        return '/customer/list'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'



class MenuItem(models.Model):
    Appetizer = 'AP'
    Entree = 'EN'
    Dessert = 'DE'
    Other = 'OT'
    MENU_TYPE_CHOICES = [
        (Appetizer, 'Appetizer'),
        (Entree, 'Entree'),
        (Dessert, 'Dessert'),       
        (Other, 'Other'),
    ]
    menu_type = models.CharField(max_length=2, choices=MENU_TYPE_CHOICES, default=Other)
    name = models.CharField(max_length=100)
    price = models.FloatField(default=0.0)
    handwork_price = models.FloatField(default=0.0)    
    create_by = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)

    def have_recipereq(self):
        return self.reciperequirement_set.count() > 0

    def get_absolute_url(self):
        return '/menuitem/list'
    
    
    def have_stock(self):
        resp = 'no stock'
        check_count = 0
        if self.have_recipereq() > 0:
            purchase_set = Purchase.objects.filter(menuitem_id=self.id).values('menuitem_id').annotate(count = Count('menuitem_id'))

            if len(purchase_set) > 0:
                for p in purchase_set:                
                    recipe = RecipeRequirement.objects.filter(menuitem_id = p['menuitem_id'])
                    for r in recipe:
                        if ((r.inventory_id.stock - r.inventory_id.used_stock) * p['count']) >= r.cant:
                            check_count = check_count + 1
                    
                    if(check_count==len(recipe)):
                        resp = 'available'
                    else:
                        resp = 'no stock'   
            else:
                resp = 'available'
        else:
            resp = 'no recipe'
        return resp
    

    def calc_price(self):
        total_price_recipe = 0
        recipe = RecipeRequirement.objects.filter(menuitem_id = self.id)
        for r in recipe:
            total_price_recipe = total_price_recipe + (r.inventory_id.price * r.cant) 
        self.price = total_price_recipe + self.handwork_price
        self.save()
    
    def __str__(self):
        return f'{self.name} - ${self.price}'

      
class RecipeRequirement(models.Model):
    inventory_id = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    menuitem_id = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    cant = models.IntegerField(default=0)

    class Meta:
        unique_together = ['inventory_id','menuitem_id']    
   
    def __str__(self):
        return f'({self.menuitem_id.name}) -  {self.inventory_id.ingredient} ({self.cant})'   



class Purchase(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    menuitem_id = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    day = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)    

    def __str__(self):
        return f'#{self.id} {self.customer_id.first_name} {self.customer_id.last_name} - {self.menuitem_id.name}, {str(self.day.day)} / {str(self.day.month)} / {str(self.day.year)}, {str(self.time)}'

    def get_absolute_url(self):
        return '/purchase/list/'   
    

    def save(self, *args, **kwargs):
        purchase_set = Purchase.objects.all().annotate(pcount = Count('menuitem_id'))

        if len(purchase_set) > 0:
            for p in purchase_set:                                      
                recipe = RecipeRequirement.objects.filter(menuitem_id = p.menuitem_id).values('inventory_id').annotate(total = Sum('cant'))
                for r in recipe:
                    Inventory.objects.filter(id=int(r['inventory_id'])).update(used_stock = (r['total'] * p.pcount))          
        
        #Change inventory stock of current purchase
        currentrecipe = RecipeRequirement.objects.filter(menuitem_id = self.menuitem_id)
        for r in currentrecipe:
            ingredient = Inventory.objects.get(id=r.inventory_id.id)
            new_cant = ingredient.used_stock + r.cant 
            Inventory.objects.filter(id=r.inventory_id.id).update(used_stock =  new_cant)         

        super(Purchase, self).save(*args, **kwargs)    


    def delete(self, using=None, keep_parents=False):          
        #Change inventory stock of current purchase
        currentrecipe = RecipeRequirement.objects.filter(menuitem_id = self.menuitem_id)
        for r in currentrecipe:
            ingredient = Inventory.objects.get(id=r.inventory_id.id)
            new_cant = ingredient.used_stock - r.cant 
            Inventory.objects.filter(id=r.inventory_id.id).update(used_stock =  new_cant)  
        
        Purchase.objects.filter(id=self.id).delete()
       
        
    


   
