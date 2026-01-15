# Library API

A **FastAPI-based** application for managing a library system  
(users, books, reservations, borrowing history), built using  
**Onion Architecture**, with **JWT authentication** and  
**asynchronous database support**.

---

## 🛠 Tech Stack

- **Python 3.12** – backend logic, OOP, asynchronous programming
- **FastAPI** – REST API, data validation (Pydantic), dependency injection
- **SQLAlchemy 2.0 (async)** – ORM, relationships, queries
- **PostgreSQL** – relational database
- **JWT / OAuth2** – authentication and user roles
- **Dependency Injector** – dependency management
- **Docker** – containerization

---

## ✨ Features

- User management (registration, update, roles, authentication)
- Book and book copy management (create, update, availability tracking)
- Book reservations and borrowing history
- Role-based authorization (`user`, `librarian`)

---

## 🚀 Getting Started

### 1. Clone the repository
git clone https://github.com/Paulina115/Biblioteka-api.git
cd library-api

### 2. Run with Docker

docker-compose up --build





