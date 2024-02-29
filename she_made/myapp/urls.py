from django.urls import path
from .views import subcategory_products, aboutus,offers,  blogs, contact,search_view, add_to_cart, view_cart, add_to_wishlist, view_wishlist, remove_from_wishlist, cart, remove_from_cart,product_detail,ShopView, ProductListView, privacy_policy, checkout, userFrofile, security_warranty, return_policy, faqs, term_condition, social_responsibility, bulk_order, update_cart, dummy

urlpatterns = [
    # for home page
    path('', ProductListView.as_view(), name='index'),  

    # for search page
    path('search/', search_view, name='search'),

    path('about-us/', aboutus, name='aboutus'),

    path('security-warranty/', security_warranty, name='security_warranty'),

    path('return-policy/', return_policy, name='return_policy'),

    path('faqs/', faqs, name='faqs'),

    path('term-condition/', term_condition, name='term_condition'),

    path('offers/', offers, name='offers'),

    path('social-responsiblity/', social_responsibility, name='social_responsibility'),

    path('bulk-orders/', bulk_order, name='bulk_order'),

    path('blogs/', blogs, name='blogs'),

    path('contact-us/', contact, name='contact'),

    path('dummy/', dummy, name='dummy'),

    path('cart/', view_cart, name='view_cart'),

    path('remove_from_cart/', remove_from_cart, name='remove_from_cart'),

    path('update-cart/', update_cart, name='update_cart'),

    path('wishlist/', view_wishlist, name='view_wishlist'),

    path('remove_from_wishlist/', remove_from_wishlist, name='remove_from_wishlist'),

    



    path('privacy-policy/', privacy_policy, name='privacy_policy'),

    path('checkout/', checkout, name='checkout'),

    path('user-profile/', userFrofile, name='user_profile'),

    # for shop page
    path('shop/', ShopView.as_view(), name='shop'),  

    # for product handling
    path('<str:sub_category>/', subcategory_products, name='subcategory_products'),
    path('<int:product_id>/<str:product_name>/', product_detail, name='product_detail'),
    
    # user cart handling pages
    path('add_to_cart/<int:item_id>/', add_to_cart, name='add_to_cart'),

    path('add_to_wishlist/<int:item_id>/', add_to_wishlist, name='add_to_wishlist'),
    
    # our static content pages
    

    
]