# ALX Travel App 0x04 – Production Deployment

## 🌍 Live Demo
[https://your-app-name.onrender.com](https://your-app-name.onrender.com)

## 🚀 Features
- Django REST Framework API
- Celery background tasks with RabbitMQ
- Swagger API documentation at `/swagger/`
- Deployed with Gunicorn on Render

## ⚙️ Environment Variables
| Variable | Description |
|-----------|--------------|
| SECRET_KEY | Django secret key |
| DEBUG | Debug mode |
| CELERY_BROKER_URL | RabbitMQ broker URL |
| CELERY_RESULT_BACKEND | Celery results backend |

## 🧠 Running Celery Worker
```bash
celery -A alx_travel_app worker -l info
