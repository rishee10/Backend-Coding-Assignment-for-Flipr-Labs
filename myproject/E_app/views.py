from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from .forms import SignUpForm, SignInForm
from .models import CustomUser, Order
from rest_framework.response import Response
from rest_framework import status, permissions, views
from django.contrib.auth.hashers import make_password
from .serializers import ProductSerializer, CartSerializer, OrderSerializer
from .models import Product
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .serializers import CartSerializer
from rest_framework.views import APIView
from .models import Cart, CartItem, Product



from .forms import SignUpForm, SignInForm, ProductForm, CartAddForm

class SignUpView(views.APIView):
    def post(self, request):
        form = SignUpForm(request.data)
        if form.is_valid():
            user = CustomUser(
                email=form.cleaned_data['email'],
                name=form.cleaned_data['name'],
                address=form.cleaned_data['address'],
                password=make_password(form.cleaned_data['password'])
            )
            user.save()
            token = RefreshToken.for_user(user)
            return Response({'message': 'User created successfully', 'user_id': user.id, 'token': str(token.access_token)}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class SignInView(views.APIView):
    def post(self, request):
        form = SignInForm(request.data)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                token = RefreshToken.for_user(user)
                return Response({'message': 'Login successful', 'token': str(token.access_token)}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)




class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.GenericAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response({'message': 'Product added successfully', 'product_id': product.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, product_id):
        product = Product.objects.get(id=product_id)
        serializer = self.get_serializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Product updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        product = Product.objects.get(id=product_id)
        product.delete()
        return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)



class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        product_id = request.data.get('product_id')
        
        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if not CartItem.objects.filter(cart=cart, product=product).exists():
            CartItem.objects.create(cart=cart, product=product)
            return Response({'message': 'Product added to cart'}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Product already in cart'}, status=status.HTTP_400_BAD_REQUEST)



class OrderView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        cart = Cart.objects.get(user=user)
        if not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
       
        order_id = 'ORD' + str(cart.id)
        cart.items.all().delete()  
        return Response({'message': 'Order placed successfully', 'order_id': order_id}, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        
        return Response({'message': 'Retrieve orders for user'}, status=status.HTTP_200_OK)



def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = CustomUser(
                email=form.cleaned_data['email'],
                name=form.cleaned_data['name'],
                address=form.cleaned_data['address'],
                password=make_password(form.cleaned_data['password'])
            )
            user.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = SignUpForm()
    return render(request, 'shop/signup.html', {'form': form})





def signin_view(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('product_list')
            else:
                form.add_error(None, "Invalid email or password.")
    else:
        form = SignInForm()
    return render(request, 'shop/signin.html', {'form': form})



def add_product_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'shop/add_product.html', {'form': form})

def add_to_cart_view(request):
    if request.method == 'POST':
        form = CartAddForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            cart, created = Cart.objects.get_or_create(user=request.user)
            product = Product.objects.get(id=product_id)
            if not CartItem.objects.filter(cart=cart, product=product).exists():
                CartItem.objects.create(cart=cart, product=product)
            return redirect('cart')
    else:
        form = CartAddForm()
    return render(request, 'shop/add_to_cart.html', {'form': form})


class OrderView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        cart = Cart.objects.get(user=user)
        if not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        order = Order.objects.create(
            user=user,
            shipping_address=user.address
        )
        # Add cart items to order (this is simplified)
        for item in cart.items.all():
            # You can add more details here for the order item if needed
            # Example: OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
            pass
        cart.items.all().delete()  # Clear cart after placing the order
        return Response({'message': 'Order placed successfully', 'order_id': order.id}, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        orders = Order.objects.filter(user=user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

