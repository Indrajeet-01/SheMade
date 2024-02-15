from django.urls import path
from .views import subcategory_products, aboutus,  blogs, contact,search_view, add_to_cart, view_cart, cart, remove_from_cart,product_detail,ShopView, ProductListView

urlpatterns = [
    # for home page
    path('', ProductListView.as_view(), name='index'),  

    # for search page
    path('search/', search_view, name='search'),

    path('about-us/', aboutus, name='aboutus'),

    path('blogs/', blogs, name='blogs'),

    path('contact-us/', contact, name='contact'),

    path('cart/', view_cart, name='view_cart'),

    path('remove_from_cart/', remove_from_cart, name='remove_from_cart'),

    # for shop page
    path('shop/', ShopView.as_view(), name='shop'),  

    # for product handling
    path('<str:sub_category>/', subcategory_products, name='subcategory_products'),
    path('<int:product_id>/<str:product_description>/', product_detail, name='product_detail'),
    
    # user cart handling pages
    path('add_to_cart/<int:item_id>/', add_to_cart, name='add_to_cart'),


    # our static content pages
    # path('abc/', aboutus, name='aboutus'),
           # for blogs page
    


    
]