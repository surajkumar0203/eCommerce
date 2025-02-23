# 🛍️ E-Commerce Website

A full-featured E-Commerce web application built with **Django**. It supports real-time order tracking, product management, email notifications, payment integration, and a role-based authentication system for both **customers** and **shopkeepers**.

## 🚀 Features

- **Real-time order tracking** using **WebSockets**
- **Redis** as an in-memory database for caching (Port: `6379`)
- **PostgreSQL** for data storage (Port: `5432`)
- **Celery** for sending invoice emails asynchronously, using Redis for caching
- **Razorpay Payment Integration** for secure online payments
- Role-based login system:
  - **Customer:** Buy products, make payments, track orders, download invoices (PDF sent via email using Celery)
  - **Shopkeeper:** Upload products, track orders
- Email verification link sent upon registration (required for account activation)
- Full-text search with **TrigramSimilarity** and filters
- Pagination for product listings
- **Docker** integration for containerized deployment

---

## 🛠️ Tech Stack
- **Backend:** Django, Django Channels
- **Database:** PostgreSQL
- **Caching:** Redis
- **Task Queue:** Celery
- **Payment Gateway:** Razorpay
- **WebSockets:** Django Channels
- **Containerization:** Docker

---

## 🐳 Docker Configuration
In your `settings.py`, configure channels:
```python
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis_queue", 6379)]  # For Docker
        },
    },
}
```

Without Docker:
```python
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)]
        },
    },
}
```

---

## 📸 Screenshots

- **Home Page:** `screenshots/Homepage.png`
- **Customer Dashboard:** `screenshots/customer_dashboard.png`
- **Shopkeeper Dashboard:** `screenshots/shopkeeper_dashboard.png`
- **Order Tracking:** `screenshots/order_tracking.png`
- **Payment Page:** `screenshots/payment_page.png`

Include them in the README like:
```markdown
![Home_Page](https://github.com/surajkumar0203/eCommerce/blob/branch1/screenshorts/Homepage.png?raw=true)
![Order Tracking](screenshots/order_tracking.png)
![Payment Page](screenshots/payment_page.png)
```

---

## 🏁 Getting Started
### Prerequisites
- Docker
- Python 3.9+
- PostgreSQL
- Redis
- Razorpay Account (for payment integration)

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```

3. **Build and run using Docker:**
   ```bash
   docker-compose up --build
   ```

4. **Apply migrations:**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Create a superuser:**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. **Run the server:**
   ```bash
   docker-compose up
   ```

### Without Docker
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run Redis and PostgreSQL manually**
3. **Apply migrations and run the server:**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

---



