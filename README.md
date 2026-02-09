# Mini Ledger API

A simple REST API built with **Django + Django REST Framework** to manage customers and their credit/debit ledger entries.

---

## Features

* User Registration & JWT Authentication
* Customer CRUD (user-specific data)
* Ledger Entries (credit/debit)
* Filter by:

  * Customer
  * Entry type
  * Date range
* Customer Summary:

  * Total Credit
  * Total Debit
  * Balance calculation

---

## Tech Stack

* Python
* Django
* Django REST Framework
* SQLite
* SimpleJWT

---

## Setup Instructions

```bash
git clone <repo-url>
cd ledger
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## Authentication

### Register

`POST /app/register/`

```json
{
  "username": "testuser",
  "password": "123456"
}
```

### Login

`POST /api/token/`

Use **access token** as Bearer token.

---

## API Endpoints

### Customers

* `POST /app/customers/`
* `GET /app/customers/`
* `PUT /app/customers/{id}/`
* `DELETE /app/customers/{id}/`

### Ledger Entries

* `POST /app/entries/`
* `GET /app/entries/?customer=1`
* `GET /app/entries/?type=credit`
* `GET /app/entries/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`

### Customer Summary

* `GET /app/customers/{id}/summary/`

Response:

```json
{
  "total_credit": 800,
  "total_debit": 200,
  "balance": 600
}
```

---

## Notes

* Users can only access their own data.
* Credit = money customer owes.
* Debit = payment received.
