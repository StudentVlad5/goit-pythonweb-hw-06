# University Management System

A comprehensive database management tool built with Python, SQLAlchemy ORM, and PostgreSQL. This project demonstrates advanced database relationships, automated data seeding, and interactive CLI interfaces for both analytics and data management.

## Tech Stack

- Language: Python 3.10+

- Database: PostgreSQL (via Docker)

- ORM: SQLAlchemy 2.0+

- Migrations: Alembic

- Data Generation: Faker

- Driver: psycopg2-binary

## Getting Started

1. Database Setup (Docker)
   Run a PostgreSQL instance using the following command:

```
docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres
```

2. Installation
   Clone the repository and install the required dependencies:

```
pip install sqlalchemy psycopg2-binary faker
```

3. Initialize Tables
   The system automatically creates tables upon the first run of the seed or CRUD scripts. However, if you are using migrations:

```
alembic upgrade head
```

## Project Components

1. Data Seeding (seed.py)
   Populates the database with realistic random data (30-50 students, 3 groups, 5-8 subjects, and 3-5 teachers).

```
python seed.py
```

Note: This script will verify table existence before insertion.

2. Analytical Reports (analytical_bot.py)
   An interactive bot to execute 12 predefined complex SQL queries.

```
python analytical_bot.py
```

### Features:

Top 5 Students: Find leaders by average grade.

Group Analytics: Average grades per subject for specific groups.

Teacher/Student tracking: Lists courses and performance metrics.

Dynamic Selection: Instead of typing long names, you select entities (students, teachers, etc.) by their list number.

3. CRUD Manager (crud_bot.py)
   A full-cycle management tool to Create, Read, Update, and Delete records.

```
python crud_bot.py
```

Functionality:

Cascade Deletion: Deleting a Group automatically removes associated Students and their Grades, maintaining database integrity.

Interactive Input: Step-by-step prompts for adding new records (e.g., when creating a Grade, it asks you to pick a Student and a Subject from a list).

## File Structure

File Description
models.py SQLAlchemy models defining the DB schema (Student, Group, Teacher, Subject, Grade).
db.py Database engine configuration and session management.
seed.py Script using Faker to populate the database.
my_select.py Core logic for the 12 analytical SQL queries.
analytical_bot.py Interactive CLI for viewing reports.
main.py Interactive CLI for manual data management.

## Database Schema Logic

The database follows a relational structure:

Groups have many Students.
Teachers have many Subjects.
Grades link Students and Subjects with a specific value and timestamp.

## Troubleshooting

**UndefinedTable Error:** Occurs if the database is empty. Run python seed.py to generate the schema and data.

**Connection Refused:** Ensure your Docker container is running (docker ps). If not, run docker start some-postgres.

**DuplicateAlias:** This error has been mitigated in my_select.py by optimizing JOIN operations to avoid redundant table declarations.
