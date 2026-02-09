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
git clone https://github.com/sibgatullah-py/ledger.git
cd ledger
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## Postman Collection

To quickly test all API endpoints, import the provided Postman collection:

- File: `ledger/Mini Leadger API.postman_collection.json`
- How to use: Open Postman, click "Import", and select the file above. All endpoints and sample requests are included.

---

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
* `GET /app/entries/?customer=2`
* `GET /app/entries/?type=credit`
* `GET /app/entries/?start_date=2026-01-01&end_date=2026-02-10`

### Customer Summary

* `GET /app/customers/1/summary/`

Response:

```json
{
    "total_credit": 800.0,
    "total_debit": 325.0,
    "balance": 475.0
}

```

---


## Additional Notes

- Users can only access their own data.
- Credit = money customer owes.
- Debit = payment received.
- Pagination is enabled for list endpoints (default page size: 10).
- Unit tests: Only a placeholder is included; full test coverage is not provided.
- Docker setup: Not included in this version.
