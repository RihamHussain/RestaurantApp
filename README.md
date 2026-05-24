# 🍽️ RestaurantApp

A full-stack Restaurant Order Management API built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**. Features cookie-based JWT authentication, role-based access control, and is fully containerized with Docker.

---

## ✨ Features

- **Authentication** — Register, login, and logout with secure HTTP-only cookie-based JWT tokens
- **Role-Based Access Control** — Three tiers: `customer`, `admin`, and `superadmin`
- **Order Management** — Customers can create, view, update, and delete their own orders
- **Admin Panel** — Admins can view and delete all orders and manage users
- **SuperAdmin Controls** — Promote/demote users to admin, delete admin accounts
- **CI/CD Pipeline** — Automated testing on every push via GitHub Actions
- **Dockerized** — One command to run the entire application

---

## 🛠️ Tech Stack

| Layer        | Technology                        |
|--------------|-----------------------------------|
| Backend      | FastAPI, Python 3.12              |
| Database     | PostgreSQL 15                     |
| ORM          | SQLAlchemy 2.0                    |
| Migrations   | Alembic                           |
| Auth         | JWT (python-jose), Passlib/bcrypt |
| Templates    | Jinja2                            |
| Testing      | Pytest, pytest-asyncio            |
| Container    | Docker, Docker Compose            |
| CI/CD        | GitHub Actions                    |

---

## 🚀 Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running
- Git

### 1. Clone the repository

```bash
git clone https://github.com/RihamHussain/RestaurantApp
cd RestaurantApp
```

### 2. Set up environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```env
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_DB=restaurant_db
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
```

> **Tip:** Generate a strong secret key with `openssl rand -hex 32`

### 3. Start the application

```bash
docker compose up --build
```

The app will be available at **http://localhost:8000**

---

## 📁 Project Structure

```
RestaurantApp/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI pipeline
├── Restaurant_App/
│   ├── routers/
│   │   ├── auth.py             # Login, register, logout
│   │   ├── orders.py           # Order CRUD endpoints
│   │   ├── users.py            # User profile endpoints
│   │   └── admin.py            # Admin management endpoints
│   ├── templates/              # Jinja2 HTML templates
│   ├── static/                 # Static files (CSS, JS, images)
│   ├── test/
│   │   ├── test_auth.py
│   │   ├── test_orders.py
│   │   ├── test_users.py
│   │   ├── test_admin.py
│   │   ├── test_main.py
│   │   └── utils.py            # Test fixtures and setup
│   ├── helpers/
│   │   └── config.py           # Settings / environment config
│   ├── __init__.py
│   ├── database.py             # SQLAlchemy engine and session
│   ├── models.py               # Database models
│   └── main.py                 # FastAPI app entry point
├── alembic/                    # Database migration files
├── alembic.ini                 # Alembic configuration
├── .env                        # Your local secrets (never committed)
├── .env.example                # Environment variable template
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── pytest.ini
└── requirements.txt
```

---

## 🔌 API Endpoints

### Auth — `/auth`

| Method | Endpoint          | Description              | Access  |
|--------|-------------------|--------------------------|---------|
| GET    | `/auth/login`     | Login page               | Public  |
| GET    | `/auth/register`  | Register page            | Public  |
| POST   | `/auth/register`  | Create new account       | Public  |
| POST   | `/auth/token`     | Login and get JWT cookie | Public  |
| POST   | `/auth/logout`    | Clear session cookie     | Auth    |
| GET    | `/auth/me`        | Get current user info    | Auth    |

### Orders — `/order`

| Method | Endpoint                      | Description              | Access   |
|--------|-------------------------------|--------------------------|----------|
| GET    | `/order/`                     | Orders page (HTML)       | Customer |
| GET    | `/order/list`                 | Get my orders (JSON)     | Customer |
| POST   | `/order/orders`               | Create a new order       | Customer |
| GET    | `/order/orders/{id}`          | Get a specific order     | Customer |
| PUT    | `/order/orders/{id}`          | Update an order          | Customer |
| DELETE | `/order/orders/{id}`          | Delete an order          | Customer |
| PUT    | `/order/orders/{id}/status`   | Update order status      | Customer |

### Users — `/user`

| Method | Endpoint                       | Description              | Access   |
|--------|--------------------------------|--------------------------|----------|
| GET    | `/user/`                       | Get my profile           | Auth     |
| PUT    | `/user/password`               | Change password          | Auth     |
| PUT    | `/user/phonenumber/{number}`   | Change phone number      | Auth     |

### Admin — `/admin`

| Method | Endpoint                  | Description                    | Access     |
|--------|---------------------------|--------------------------------|------------|
| GET    | `/admin/orders`           | Get all orders                 | Admin      |
| DELETE | `/admin/orders/{id}`      | Delete any order               | Admin      |
| GET    | `/admin/users`            | Get all users                  | Admin      |
| DELETE | `/admin/users/{id}`       | Delete a user                  | Admin      |
| PUT    | `/admin/promote/{id}`     | Promote user to admin          | SuperAdmin |
| PUT    | `/admin/demote/{id}`      | Demote admin to customer       | SuperAdmin |

---

## 👥 Role Hierarchy

```
SuperAdmin
    └── Can promote/demote admins
    └── Can delete admin accounts
    └── Cannot be deleted via API

Admin
    └── Can view/delete all orders
    └── Can view/delete customer accounts
    └── Cannot delete other admins

Customer
    └── Can manage their own orders only
    └── Can update their own profile
```

---

## 🧪 Running Tests

Tests use a separate PostgreSQL test database (configured via `SQLALCHEMY_TEST_DATABASE_URL`).

### Locally

```bash
# Make sure your .env is configured, then:
pytest
```

### In Docker

```bash
docker compose exec app pytest
```

### CI

Tests run automatically on every push and pull request to `main` via GitHub Actions.

---

## 🗄️ Database Migrations

Migrations are managed with Alembic.

```bash
# Apply all migrations
docker compose exec app alembic upgrade head

# Create a new migration after changing models
docker compose exec app alembic revision --autogenerate -m "your message"

# Roll back one migration
docker compose exec app alembic downgrade -1
```

---

## 🐳 Docker Commands

```bash
# Start everything
docker compose up --build

# Start in background
docker compose up --build -d

# Stop containers
docker compose down

# Stop and remove database volume (full reset)
docker compose down -v

# View logs
docker compose logs -f

# View app logs only
docker compose logs -f app
```

---

## ⚙️ Environment Variables

| Variable                    | Description                          | Example                                      |
|-----------------------------|--------------------------------------|----------------------------------------------|
| `POSTGRES_USER`             | PostgreSQL username                  | `myuser`                                     |
| `POSTGRES_PASSWORD`         | PostgreSQL password                  | `mypassword`                                 |
| `POSTGRES_DB`               | Database name                        | `restaurant_db`                              |
| `SECRET_KEY`                | JWT signing secret                   | `openssl rand -hex 32`                       |
| `ALGORITHM`                 | JWT algorithm                        | `HS256`                                      |
| `SQLALCHEMY_DATABASE_URL`   | Full database connection string      | `postgresql+psycopg2://user:pass@db:5432/db` |
| `SQLALCHEMY_TEST_DATABASE_URL` | Test database connection string   | Same format, different DB name               |

---

## 🔒 Security Notes

- Passwords are hashed with **bcrypt**
- JWT tokens are stored in **HTTP-only cookies** (not accessible via JavaScript)
- `secure=True` is enabled automatically in production (Render)
- New registrations are always assigned the `customer` role regardless of input
- SuperAdmin accounts cannot be deleted via the API

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👩‍💻 Author

Built from scratch by **Riham Hussain**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Riham%20Hussain-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/riham-a-hussain/)