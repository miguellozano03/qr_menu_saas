# 🍽️ Menu SaaS

<sub>⚠️ This project is under active development</sub>

A SaaS platform to manage digital restaurant menus with authentication, modular architecture, and scalable backend design.

---

## 🚀 Features

* JWT Authentication (register, login)
* User account management (`/me`)
* Modular architecture (router → service → repository)
* Centralized exception handling
* Database migrations with Alembic
* Unit tests for security layer

---

## 🛠 Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* Pytest

---

## 📖 API Preview
![API DOCS](/docs/assets/swagger.png)


## 📂 Project Structure

```bash id="s1t2p3"
apps/
  api/
    app/
      core/        # config, db, security, exceptions
      modules/     # users, restaurants
      api/v1/      # routes
      shared/      # shared utilities
    tests/         # unit tests
  web/             # frontend (in progress)
  landing/         # landing page (in progress)
```

---

## ⚙️ Installation & Run

```bash id="run1"
cd apps/api
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 🔐 Environment Variables

Create a `.env.dev` file:

```env id="env1"
DB_MOTOR=postgresql
DB_DRIVER_ASYNC=asyncpg
DB_DRIVER_SYNC=psycopg2
DB_USER=dev
DB_PASSWORD=dev
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=menuqr_dev_db

SECRET_KEY=QWERTYUIOPASDFGHJKLZXCVBNM1234567890abcdefABCDEFGH
```

---

## 📖 API Documentation

Interactive docs available at:

* Swagger UI:

```
/docs
```

* ReDoc:

```
/redoc
```

---

## 🧪 Running Tests

```bash id="test1"
pytest apps/api/tests/
```

✔ All tests should pass before deployment.

---

## 🧾 Test Coverage

Current tests include:

* JWT service
* Password service

---

## 🚧 Status

<sub>This project is under active development. Some modules and the frontend are still in progress.</sub>

---

## 🎯 Purpose

This project is built as a real-world SaaS backend and portfolio project to demonstrate:

* Clean architecture
* Authentication & security
* Scalable API design
* Testing practices
