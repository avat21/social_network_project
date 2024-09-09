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

### Configuration
JWT Secret Key: Ensure you set a strong secret key in your environment variables. Update the SECRET_KEY in your .env file or Docker environment.

Database: By default, the project uses SQLite. Modify settings.py to configure other databases like PostgreSQL or MySQL if needed.

