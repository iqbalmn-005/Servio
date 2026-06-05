# Servio (Service 1)

This is a Django-based web application.

## Prerequisites

- Python 3.x
- pip

## Getting Started

Follow these instructions to set up the project locally.

### 1. Clone the repository

```bash
git clone <repository-url>
cd service1
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```
Activate the environment:
- **Windows**: `venv\Scripts\activate`
- **macOS/Linux**: `source venv/bin/activate`

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Create a `.env` file in the root directory (alongside `manage.py`) to store your configuration settings such as database credentials and secret keys. 

### 5. Apply Migrations

```bash
python manage.py migrate
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000/`.

## Project Structure

- `service1/`: Main project configuration directory
- `user/`: User management application
- `provider/`: Provider application
- `services/`: Services application
