from django.urls import path
from .views import subcategory_products, about_us, SearchProduct,  blogs, contact,search_view, add_to_cart, view_cart, remove_from_cart,product_detail,search_results_view ,ShopView, ProductListView

urlpatterns = [
    

    path('', ProductListView.as_view(), name='index'),

    path('search/', SearchProduct.as_view(), name='search'),

    path('search/results/', search_results_view, name='search_results'),

    path('shop/', ShopView.as_view(), name='shop'),  # Base URL for shop

    path('<str:sub_category>/', subcategory_products, name='subcategory_products'),
    
    path('<int:product_id>/<str:product_description>/', product_detail, name='product_detail'),
    # path('cart/', cart, name='cart'),
    path('about-us/', about_us, name='about_us'),
    path('blogs/', blogs, name='blogs'),
    path('contact-us/', contact, name='contact'),

    path('add_to_cart/<int:item_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('remove_from_cart/', remove_from_cart, name='remove_from_cart'),

    
]