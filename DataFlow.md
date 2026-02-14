# Mini Ledger API

A RESTful backend service built using Django and Django REST Framework that allows authenticated users to manage customers and their credit/debit ledger entries securely.

This project demonstrates authentication, database relationships, filtering, and financial summary logic.

---

## Core Features

* User Registration & Login (JWT Authentication)
* Customer CRUD Operations
* Ledger Entry Management ( Credit/Debit)
* Filtering by customer, type, and date range
* Customer Financial Summary
* User-specific data isolation
* Pagination support

---

# System Flow Overview
* The system is divided into four logical flows:
    * Authentication flow
    * Customer Management flow
    * Ledger Entry flow
    * Customer Summery flow


## Part-1 Authentication flow

```bash
User → Register API → Database(User)
User → Login API → JWT Token → Protected APIs
```

* Explanation:
    * Register:
        - User sends username + password
        - Django creates user in DB
    
    * Login:
        - User sends credentials (username, password)
        - System returns Access Token (JWT)

    * Protected APIs:
        - Token goes in header → Backend verifies (JWT) → Access granted

```bash
[User]
   ↓
POST /register
   ↓
[User Table]



[User]
   ↓
POST /api/token
   ↓
[JWT Access Token]
   ↓
Authorization: Bearer <token>
   ↓
[Customers / Entries APIs]

```

* Endpoints:
    * POST  /app/register/------| Registering New User
    * POST  /api/token/---------| Generating token for Login
    * POST  /api/token/refresh/-| Refreshing token for stop continuous login

* Why two different prefix?
    * /app/ ---> Custom business APIs (customer, ledger)
    * /api/ ---> Authentication/System APIs

* Login token generator:
    ```bash
    User sends username + password 
    ↓ 
    Django verifies credentials
    ↓
    If correct returns:
    {
        "refresh":"long_token",
        "access":"short_token",
    }
    ```

* Refresh Token:
    When access token expires, User sends refresh token, Django takes that refresh token and gives a new access token.

    Note: Refresh Token helps to avoid forcing user to login again and again.

* Logic:
    * Registration creates a new user.
    * Login returns an access token
    * All protected routes returns:
        ```bash
        Authorization: Bearer<access_token>
        ```

## Part-2 Customer Management flow

```bash
User -> Customer API -> Customer Table(DB)
```

* Diagram:
```bash
[Authenticated User]
   ↓
[Create | List | Update | Delete]
   ↓
[Customer Model]
   ↓
[user_id attached automatically]

```
* Idea:-> 
    * Every customer row has an user_id column so no user can see another user's customers.

 ```bash
    from django.urls import path
    from rest_framework.routers import DefaultRouter
    from .views import CustomerViewSet, RegisterView, LedgerEntryViewSet

    # DefaultRouter is a DRF tool that auto-creates REST URLs.
    router = DefaultRouter()# Creating and empty router object.
    
    # viewSets are plugged in the router Object.
    router.register(r'customers', CustomerViewSet, basename='customers')
    router.register(r'entries', LedgerEntryViewSet, basename='entries')


    # path is normal Django URL
    urlpatterns = [
        path('register/', RegisterView.as_view()), # not a view set
    ] + router.urls

```

path = normal Django URL
DefaultRouter = DRF tool that auto-creates REST URLs
```bash
router = DefaultRouter()
```
This creates and empty router object. ViewSets are plugged into it

* Registering ViewSets:
```bash
router.register(r'customers', CustomerViewSet, basename='customers')
```
This powerful path telling Django:
"For Customers, use CustomerViewSet and automatically generate all CRUD URLs"
So instead of writing different urls for each function in CRUD, the router does all the work(generating urls).

* basename
```bash
basename='customers'
```
This is just an internal name DRF uses for reversing URLs, required when no queryset is defined directly.

* The end points this router objects creates:
```bash
GET    /app/customers/              List
POST   /app/customers/              Create
GET    /app/customers/{id}/         Retrieve
PUT    /app/customers/{id}/         Update
PATCH  /app/customers/[id]/         Partial Update
DELETE /app/customers/{id}/         Delete
GET    /app/customers/{id}/summery/ Custom actions
```

* End points used in project 
```bash
POST  /app/customers/
GET   /app/customers/
PUT   /app/customers/{id}/
DELETE /app/customers/{id}/
```

* Logic:
    * Every customer newly created is automatically linked to the logged in user.
    * One user cannot access other user's customers


## Part-3 Ledger Entry Flow
```bash
User -> Ledger API -> LedgerEntry Table DB -> Linked Customers
```

* Diagram:
```bash
[User]
   ↓
[POST /entries]
   ↓
[LedgerEntry]
   ├── type (credit/debit)
   ├── amount
   ├── date
   ├── user_id
   └── customer_id

```

* Relationships:
```bash
User 1 ───< Customer ───< LedgerEntry
```
    *Meaning:
        * One user --> many customers
        * One customers --> many ledger entries

* Fields:
    * type (credit/debit)
    * amount
    * note
    * entry_date
    * user_id
    * customer_id

* End Points:
    ```bash
    POST /app/entries/
    GET  /app/entries/
    ```

* Filters:
    * By Customers = ?customer=1
    * By type      = ?type=credit
    * By date      = ?start_date=yyyy_mmmm_dddd


## Part-4 Customer Summery Logic
Only calculation
```bash
[GET /customers/{id}/summary]
   ↓
[Filter entries by customer+user]
   ↓
[Aggregate Sum]
   ↓
[Return Total]
```

Diagram
```bash
[customer]
   ↓
[Fetch Ledger Entries]
   ↓
[Sum Credit/Sum Debit]
   ↓
[Balance = Credit - Debit]
   ↓
[JSON Response]
```

* End point
```bash
GET /app/customers/{id}/summery/
```