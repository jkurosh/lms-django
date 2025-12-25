# 🐾 VetLMS - Veterinary Learning Management System

<div align="center">

![VetLMS](https://img.shields.io/badge/VetLMS-Veterinary%20LMS-blue?style=for-the-badge)
![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)

**A comprehensive Learning Management System designed specifically for veterinary education**

[Features](#-features) • [Installation](#-installation) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 📖 About

**VetLMS** is a specialized Learning Management System (LMS) for veterinary education that enables students and professionals to learn through real-world case studies, interactive tests, and advanced diagnostic tools.

Built with Django and modern web technologies, this platform provides an interactive and effective learning experience with a scalable architecture.

## ✨ Features

### 📚 Interactive Case Studies
- **Comprehensive Case Library**: Extensive collection of real veterinary case studies
- **Laboratory Test Analysis**: Interactive analysis of CBC, clinical chemistry, and morphological changes
- **Diagnostic Tools**: Advanced system for analyzing and interpreting laboratory results
- **Smart Categorization**: Organized case studies by different categories and specialties
- **Progress Tracking**: Track your learning progress and completion status

### 👥 User Management
- **Complete Authentication**: Registration, login, and password recovery system
- **User Profiles**: Comprehensive user profile management
- **Bookmarking**: Save favorite case studies for later review
- **Achievement System**: Track achievements and milestones

### 💳 Payment Integration
- **Payment Gateway**: Integrated payment gateway support
- **Subscription Plans**: Flexible subscription plan management
- **Shopping Cart**: Complete shopping cart functionality
- **Transaction History**: Full transaction tracking and history

### 📊 Admin Dashboard
- **Comprehensive Analytics**: Detailed statistics and reports
- **Case Management**: Add, edit, and manage case studies
- **User Management**: Complete user and access management
- **Reporting**: Detailed activity and usage reports

### 🔒 Security
- **Content Security Policy (CSP)**: Protection against XSS attacks
- **Rate Limiting**: Request throttling to prevent abuse
- **CSRF Protection**: Built-in CSRF protection for all forms
- **Secure Authentication**: Secure password hashing and storage
- **XSS Protection**: Protection against script injection attacks

### 🌐 Internationalization
- **Persian Language Support**: Full RTL support for Persian/Farsi
- **Jalali Date Support**: Persian calendar integration using jdatetime
- **SMS Integration**: SMS notification support for local services

## 🛠️ Tech Stack

### Backend
- **Django 5.2**: High-level Python web framework
- **Django REST Framework**: Powerful toolkit for building Web APIs
- **PostgreSQL 16**: Advanced open-source relational database
- **Redis**: In-memory data structure store (optional, for caching)
- **Gunicorn**: Python WSGI HTTP Server for production

### Frontend
- **HTML5 & CSS3**: Modern web standards
- **JavaScript**: Vanilla JavaScript for client-side interactions
- **Tailwind CSS**: Utility-first CSS framework
- **Responsive Design**: Mobile-first responsive design

### DevOps & Infrastructure
- **Docker**: Containerization platform
- **Docker Compose**: Multi-container Docker application management
- **Nginx**: High-performance web server and reverse proxy
- **Git**: Distributed version control system

### Integrations
- **Payment Gateway**: Online payment gateway integration
- **SMS Services**: SMS notification services
- **Email Services**: Email notification support

## 🚀 Quick Start

### Prerequisites

- Python 3.12 or higher
- PostgreSQL 16 or higher
- Docker and Docker Compose (recommended for easy setup)
- Git

### Installation with Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/jkurosh/vetlms.git
   cd vetlms
   ```

2. **Setup environment variables**
   ```bash
   cp env.docker.example .env
   # Edit .env file with your configuration
   ```

3. **Build and start containers**
   ```bash
   make build
   make up
   ```

4. **Run database migrations**
   ```bash
   make migrate
   ```

5. **Create superuser**
   ```bash
   make createsuperuser
   ```

6. **Access the application**
   - Web Interface: http://localhost
   - Admin Panel: http://localhost/admin

### Installation without Docker

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup database**
   ```bash
   # Create PostgreSQL database
   createdb vetlms_db
   
   # Run migrations
   python manage.py migrate
   ```

4. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

## 📁 Project Structure

```
vetlms/
├── apps/
│   ├── courses/          # Case study management
│   │   ├── models.py     # Data models
│   │   ├── views.py      # View functions
│   │   ├── api_views.py  # API endpoints
│   │   └── templates/    # HTML templates
│   │
│   ├── users/            # User management
│   │   ├── models.py     # User and profile models
│   │   ├── auth_views.py # Authentication views
│   │   ├── views.py      # User views
│   │   └── services/     # Payment and SMS services
│   │
│   └── core/             # Shared utilities
│
├── vetlms/               # Django project settings
│   ├── settings.py       # Settings (requires .env)
│   ├── urls.py           # URL routing
│   └── wsgi.py           # WSGI configuration
│
├── static/               # Static files (CSS, JS, images)
├── templates/            # Base templates
├── media/                # User uploaded files
│
├── Dockerfile            # Docker image definition
├── docker-compose.yml    # Docker Compose configuration
├── nginx.conf            # Nginx configuration
├── requirements.txt      # Python dependencies
└── Makefile              # Development commands
```

## 🎯 Available Commands

Using the `Makefile`, you can run the following commands:

```bash
make help              # Show all available commands
make setup             # Initial setup (copy .env file)
make build             # Build Docker images
make up                # Start all services
make down              # Stop all services
make restart           # Restart all services
make migrate            # Run database migrations
make makemigrations     # Create new migrations
make shell              # Access Django shell
make test               # Run tests
make logs               # View container logs
make backup-db          # Backup database
make collectstatic      # Collect static files
```

## 📚 API Documentation

The project uses Django REST Framework for API endpoints:

- **Case Studies API**: `/api/v1/` - Case study related endpoints
- **Authentication API**: `/api/v1/auth/` - User authentication endpoints
- **Payment API**: `/api/v1/payment/` - Payment processing endpoints

### Example API Request

```bash
# Get case studies
curl http://localhost/api/v1/cases/

# Authenticate user
curl -X POST http://localhost/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'
```

## 🔐 Security Best Practices

This project implements several security measures:

- ✅ **SECRET_KEY** stored in environment variables
- ✅ **Rate Limiting** to prevent brute force attacks
- ✅ **CSP Headers** for XSS protection
- ✅ **CSRF Protection** in all forms
- ✅ **SQL Injection Protection** using Django ORM
- ✅ **Password Hashing** using PBKDF2 algorithm
- ✅ **Secure Cookies** with HttpOnly and Secure flags
- ✅ **HTTPS Enforcement** in production

## 🧪 Testing

Run tests using:

```bash
# With Docker
make test

# Without Docker
python manage.py test
```

## 📝 Environment Variables

Create a `.env` file with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB_NAME=vetlms_db
POSTGRES_DB_USER=vetlms_user
POSTGRES_DB_PASSWORD=your-password
POSTGRES_DB_HOST=db
POSTGRES_DB_PORT=5432

# Payment Gateway (Optional)
ZARINPAL_MERCHANT_ID=your-merchant-id
ZARINPAL_SANDBOX=True

# SMS Service (Optional)
FARAZ_SMS_API_KEY=your-api-key
FARAZ_SMS_SENDER_NUMBER=your-sender-number
```

## 🌱 Development

### Setting up Development Environment

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Write tests for new features

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/jkurosh/vetlms/issues).

### How to Contribute

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- Django community for the excellent framework
- All contributors who have helped improve this project
- The veterinary education community for inspiration

## 📞 Support

For support, please open an issue in the GitHub repository.

---

<div align="center">

**Made with ❤️ for the Veterinary Education Community**

⭐ If you find this project useful, please give it a star!

[⬆ Back to Top](#-vetlms---veterinary-learning-management-system)

</div>
