from django.urls import path
from .views import SignUpView, SignInView, LogoutView, ProductListView, ProductDetailView, CartView, OrderView
# from .views import CartAddView
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('addproduct/', ProductDetailView.as_view(), name='add_product'),
    path('updateproduct/<int:product_id>/', ProductDetailView.as_view(), name='update_product'),
    path('deleteproduct/<int:product_id>/', ProductDetailView.as_view(), name='delete_product'),
    path('cart/', CartView.as_view(), name='cart'),
    # path('cart/add/', CartView.as_view(), name='add_to_cart'),

    path('cart/add/', CartView.as_view(), name='cart_add'),
    path('cart/delete/', CartView.as_view(), name='remove_from_cart'),
    path('placeorder/', OrderView.as_view(), name='place_order'),
    path('getorders/', OrderView.as_view(), name='get_orders'),
]
