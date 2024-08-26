# Backend-Coding-Assignment-for-Flipr-Labs

E-Commerce Project
Overview
This is an e-commerce application backend built with Django. It includes features for user authentication, product management, cart management, and order management. The application allows users to sign up, sign in, manage their shopping cart, and place orders.

Features
User Authentication:

Sign Up


Sign In

Password Hashing and Security


Product Management:

Add Product,
Update Product,
Delete Product,
View All Products



Cart Management:

Add Product to Cart,
Remove Product from Cart,
View Cart



Order Management:

Place Order,
View Orders,

Installation


Prerequisites

Code Editor

Python 3.7+

Django 3.2+

Django REST Framework

PostgreSQL or other database



Setup

Clone the Repository:


git clone https://github.com/rishee10/Backend-Coding-Assignment-for-Flipr-Labs/tree/main

cd myproject

Create a Virtual Environment:

python -m venv env

source env/bin/activate   # On Windows use `env\Scripts\activate`



Install Dependencies:

install requirements



Apply Migrations:

python manage.py migrate

Create a Superuser:

python manage.py createsuperuser

Run the Development Server:

python manage.py runserver


Usage

API Endpoints


Authentication


Sign Up

Endpoint: /signup/

Method: POST

Parameters: name, email, password, confirm_password

Response: Success message with customer ID or error message.


Sign In

Endpoint: /signin/

Method: POST

Parameters: email, password

Response: JWT token and success message or error message.


Product Management

Add Product

Endpoint: /addproduct/

Method: POST

Parameters: name, description, price, category

Response: Success message with product ID or error message.



Update Product

Endpoint: /updateproduct/<int:product_id>/

Method: PUT

Parameters: name, description, price, category

Response: Success message or error message.



Delete Product

Endpoint: /deleteproduct/<int:product_id>/

Method: DELETE

Parameters: None

Response: Success message or error message.



Get All Products

Endpoint: /products/

Method: GET

Parameters: None

Response: List of products.



Cart Management

Add Product to Cart

Endpoint: /cart/add/

Method: POST

Parameters: product_id

Response: Success message or error message.



Delete Product from Cart

Endpoint: /cart/delete/

Method: DELETE

Parameters: product_id

Response: Updated cart details or error message.

Get Cart

Endpoint: /cart/

Method: GET

Parameters: None

Response: Cart details including total amount.



Order Management

Place Order

Endpoint: /placeorder/

Method: POST

Parameters: shipping_details

Response: Order confirmation with order ID.



Get Orders

Endpoint: /getorders/

Method: GET

Parameters: None

Response: List of orders with details.


Testing


API Testing with Postman

Setting Up Postman

Open Postman and create a new collection for the project.


Testing Authentication


Sign Up:


Set up a POST request to /signup/ with required parameters.

Check for a success message or errors.


Sign In:

Set up a POST request to /signin/ with email and password.

Verify you receive a JWT token and check for errors.


Testing Product Management

Use the corresponding POST, PUT, DELETE, and GET requests for product endpoints.


Testing Cart Management

Test adding, deleting products from the cart, and retrieving cart details.


Testing Order Management

Place an order and verify the response.

Retrieve orders and verify the list of orders.

Handling Authentication in Postman


Add Authorization Header:


For authenticated requests, include the Authorization header with the value Bearer <token>.


Testing with Token:
Use the JWT obtained from the sign-in endpoint to authenticate further requests.

