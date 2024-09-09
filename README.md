# social_network_project
Welcome to the Social Network API! This project is a built with Django and Django REST Framework. We integrate JWT authentication for secure apis.

## Technologies

- **Django**: A high-level Python web framework.
- **Django REST Framework**: A powerful toolkit for building Web APIs.
- **JWT Authentication**: For secure user authentication.
- **Docker**: Containerize the application.
- **SQLite**: The default database for local development.

## Installation

### Prerequisites

- Python 3.12

### Clone the Repository

```bash
git clone https://github.com/avat21/social_network_project.git
cd social_network_project

# Build and start docker container
docker-compose up --build

# Apply migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access the api

http://localhost:8000
```

### Configuration
JWT Secret Key: Ensure you set a strong secret key in your environment variables. Update the SECRET_KEY in your .env file or Docker environment.

Database: By default, the project uses SQLite. Modify settings.py to configure other databases like PostgreSQL or MySQL if needed.

### API Endpoint

Postman api workspace link

``` bash
https://www.postman.com/interstellar-spaceship-388909/workspace/public-workspace/collection/21410520-2a59fd5c-508f-4134-9512-e31b532e04a0?action=share&creator=21410520
```
