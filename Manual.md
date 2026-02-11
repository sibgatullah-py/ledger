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
    When access token expiers, User sends refresh token, Django takes that refresh token and gives a new access token.

    Note: Refresh Token helps to avoid forcing user to login again and again.

* Logic:
    * Registration creates a new user.
    * Login returns an access token
    * All protected routes returns:
        ```bash
        Authorization: Bearer<access_token>
        ```

## Part-1 Authentication flow