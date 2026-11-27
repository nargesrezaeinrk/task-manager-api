# Veysa — Task Manager

A responsive task management application built with Django. Veysa helps users organize their tasks, track their progress, and plan their weeks through a customizable task management system and an interactive weekly planner.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Testing](#testing)
- [Future Improvements](#future-improvements)
- [License](#license)
- [Contributing](#contributing)

---

## Project Overview

Veysa was created to provide a more organized and user-friendly approach to task management.

Traditional task managers do not always provide the flexibility or visual organization users need. Veysa addresses this by combining task management with a weekly planner, allowing users to organize their responsibilities, document their progress, and keep track of their activities over time.

The application allows users to create tasks, organize them using custom labels, assign priorities, and track their progress. Users can also create multiple weekly planners, making it possible to plan their activities and revisit previous weeks.

The project was also an opportunity to explore full-stack web development, REST API design, database relationships, authentication, and responsive user interface development.

## Features

### Task Management

- Create, view, update, and delete tasks.
- Assign priorities to tasks: Low, Medium, and High.
- Track task progress through different statuses.
- Create custom labels and associate multiple labels with tasks.
- Sort tasks by priority or progress.
- Search tasks through the REST API by title or description.
- Track task creation and last-update timestamps.

### Weekly Planner

- Create multiple weekly planners.
- Organize activities using a weekly grid.
- Add and edit entries for different days and time slots.
- Save changes manually.
- Navigate between current and previously created weeks.

### User Management and Authentication

- User registration and login.
- JWT-based authentication.
- Access and refresh token management.
- Token blacklisting on logout.
- Profile management.
- Password changes.
- User-specific task access and permissions.

### User Interface

- Responsive layouts for desktop and mobile devices.
- Custom-designed interface with a focus on usability.
- Navigation across the application's main sections.
- Dedicated task management and weekly planner pages.

---

## Technologies Used

### Backend

- **Python 3.12**
- **Django 5.0**
- **Django REST Framework**
- **Simple JWT** — JWT authentication and token management.
- **PostgreSQL 16** — relational database.
- **Gunicorn** — WSGI application server.

### Frontend

- HTML5
- CSS3
- JavaScript
- Django Templates

### Development and Deployment

- Docker
- Docker Compose
- Nginx
- Git and GitHub
- Postman
- Render

---

## Project Structure

The project follows a modular Django structure, separating its main application components.

```text
task-manager-api/
│
├── apps/
│   ├── users/
│   ├── tasks/
│   ├── dashboard/
│   └── planner/
│
├── config/
│   └── ...
│
├── templates/
│   └── ...
│
├── static/
│   └── ...
│
├── nginx/
│   └── nginx.conf
│
├── postman/
│   └── ...
│
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── requirements.txt
├── .env.example
├── .gitignore
└── manage.py
```

---

## Screenshots

Screenshots of the application's interface will be added here.

### Task Manager


<!-- Will be added in the future -->

### Weekly Planner


<!-- Will be added in the future -->

### Mobile Interface

<!-- Will be added in the future -->

---

## Installation and Setup

The project uses Docker Compose to run the Django application, PostgreSQL database, and Nginx reverse proxy.

### Prerequisites

Make sure you have installed:

- [Git](https://git-scm.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### 1. Clone the Repository

```bash
git clone https://github.com/nargesrezaeinrk/task-manager-api.git
cd task-manager-api
```

### 2. Configure Environment Variables

Create a `.env` file in the project root using `.env.example` as a template.

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Update the values in your `.env` file:

```env
SECRET_KEY=your_django_secret_key

DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=task_manager
DB_USER=postgres
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
DB_ENGINE=django.db.backends.postgresql

SECURE_COOKIES=False
```

Use your own secret key and database password.

**Important:** Never commit your actual `.env` file or expose your secret key and database credentials.

### 3. Build and Start the Containers

Make sure Docker Desktop is running, then execute:

```bash
docker compose up --build
```

Docker Compose starts three services:

| Service | Description |
|---|---|
| `db` | PostgreSQL database |
| `web` | Django application running with Gunicorn |
| `nginx` | Reverse proxy and static/media file server |

The Django entrypoint waits for PostgreSQL to become available and automatically runs database migrations before starting Gunicorn.

### 4. Access the Application

Once the containers are running, open:

http://localhost

### 5. Stop the Application

To stop the running containers:

```bash
docker compose down
```

Docker volumes are retained, so your database data and uploaded files remain available when you start the containers again.

To remove the containers **and all associated named volumes**, including persistent database data, use:

```bash
docker compose down -v
```

**Warning:** This permanently deletes the data stored in those Docker volumes.

---

## Usage

### Web Application

After starting the application, users can:

1. Register an account or log in.
2. Create and organize tasks.
3. Assign priorities and custom labels.
4. Update task statuses as they make progress.
5. Sort tasks according to their priorities or progress.
6. Create weekly planners and organize activities.
7. Navigate between previously created weekly planners.

### REST API

The project also provides a REST API built with Django REST Framework.

The API supports task management operations, authentication, and task search and filtering.

#### Authentication

The API provides endpoints for:

- User registration.
- User login.
- Retrieving the authenticated user's information.
- Refreshing access tokens.
- Changing passwords.
- Logging out and blacklisting refresh tokens.

#### Task Endpoints

The API supports the following operations:

- List tasks.
- Create a task.
- Retrieve an individual task.
- Update a task.
- Partially update a task.
- Delete a task.

Additional API functionality includes:

- Searching tasks by title or description.
- Filtering tasks based on supported task attributes.

Protected endpoints require JWT authentication.

### Postman Collection

A Postman collection is included in the `postman/` directory.

It contains 13 requests organized into three folders:

| Category | Requests |
|---|---|
| Authentication | Register, Login, Get Current User, Refresh Access Token, Change Password, Logout |
| Users | Get My Profile |
| Tasks | List, Create, Retrieve, Update, Partially Update, Delete |

The collection also includes scripts for managing JWT access and refresh tokens.

To use the collection:

1. Import the collection into Postman.
2. Configure the `baseUrl` variable with your application URL.
3. Register a user and log in.
4. Use the available requests to interact with the API.

---

## Testing

### Django Automated Tests

The project includes automated tests using Django's built-in testing framework and `TestCase`.

The current tests cover:

- **Authentication:** Successful login with valid credentials.
- **Dashboard:** Access restrictions for unauthenticated users and successful access for authenticated users.
- **Profile Management:** Authentication requirements, profile updates, and password changes.
- **Task Permissions:** Ensuring users cannot access or edit tasks belonging to other users.

To run the tests inside the Docker container:

```bash
docker compose exec web python manage.py test
```

Alternatively, if running Django directly in a local Python environment:

```bash
python manage.py test
```

### API Testing

The REST API can be tested using the provided Postman collection.

The collection includes requests for authentication, user information, and task CRUD operations.

---

## Future Improvements

Planned improvements include:

- Implementing task search and filtering in the web interface.
- Expanding automated test coverage, particularly for the weekly planner.
- Further improving the user interface and mobile experience.

---

## License

The licensing and usage terms for this project are currently being finalized.

The project source code and original design assets are protected by their respective copyright owners. No general permission to reuse, redistribute, or commercially exploit them is granted at this time.

The Veysa name and branding are separate from the project's source code.

---

## Contributing

Suggestions, bug reports, and feature requests are welcome.

Please open an issue to discuss proposed changes before submitting a contribution. Formal contribution and licensing terms will be provided separately.