from django.urls import path, include

from . import views

urlpatterns = [
   path('', views.home, name='home'),
   path('account/', include('django.contrib.auth.urls'), name='login'),
   path('logout/', views.get_logout, name='logout'),
   
   #Inventory module
   path('inventory/list', views.get_inventary, name="inventorylist"),
   path('inventory/create', views.InventoryCreate.as_view(), name="inventorycreate"),
   path('inventory/update/<pk>', views.InventoryUpdate.as_view(), name="inventoryupdate"),
   path('inventory/delete/<pk>', views.InventoryDelete.as_view(), name="inventorydelete"),

   #MenuItem module
   path('menuitem/list', views.MenuItemList.as_view(), name="menuitemlist"),
   path('menuitem/create', views.MenuItemCreate.as_view(), name="menuitemcreate"),
   path('menuitem/update/<pk>', views.MenuItemUpdate.as_view(), name="menuitemupdate"),
   path('menuitem/delete/<pk>', views.MenuItemDelete.as_view(), name="menuitemdelete"),

   #RecipeRequeriment  
   path('recipereq/<menuid>/list', views.get_recipes, name="recipereqlist"),      
   path('recipereq/<menuid>/create/', views.RecipeReqCreate.as_view(), name="recipereqcreate"),
   path('recipereq/<menuid>/update/<pk>', views.RecipeReqUpdate.as_view(), name="reciperequpdate"),
   path('recipereq/<menuid>/delete/<pk>', views.RecipeReqDelete.as_view(), name="recipereqdelete"), 

   #Customer module
   path('customer/list', views.CustomerList.as_view(), name="customerlist"),
   path('customer/create', views.CustomerCreate.as_view(), name="customercreate"),
   path('customer/update/<pk>', views.CustomerUpdate.as_view(), name="customerupdate"),
   path('customer/delete/<pk>', views.CustomerDelete.as_view(), name="customerdelete"),

   #Purchase module 
   path('purchase/<customerid>/list', views.get_purchases_customer, name="purchaselistcustomer"),   
   path('purchase/list/', views.get_purchases, name="purchaselist"),     
   path('purchase/create', views.PurchaseCreate.as_view(), name="purchasecreate"),
   path('purchase/update/<pk>', views.PurchaseUpdate.as_view(), name="purchaseupdate"),
   path('purchase/delete/<pk>', views.PurchaseDelete.as_view(), name="purchasedelete"), 

  
 
]