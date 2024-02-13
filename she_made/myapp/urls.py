from django.urls import path
from .views import subcategory_products, about_us,  blogs, contact,search_view, add_to_cart, view_cart, remove_from_cart,product_detail,ShopView, ProductListView

urlpatterns = [
    # for home page
    path('', ProductListView.as_view(), name='index'),  

    # for search page
    path('search/', search_view, name='search'),

    # for shop page
    path('shop/', ShopView.as_view(), name='shop'),  

    # for product handling
    path('<str:sub_category>/', subcategory_products, name='subcategory_products'),
    path('<int:product_id>/<str:product_description>/', product_detail, name='product_detail'),
    
    # user cart handling pages
    path('add_to_cart/<int:item_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'), # for cart page
    path('remove_from_cart/', remove_from_cart, name='remove_from_cart'),

    # our static content pages
    path('about-us/', about_us, name='about_us'), # for about us page
    path('blogs/', blogs, name='blogs'),         # for blogs page
    path('contact-us/', contact, name='contact'), # for contact us page

    
]