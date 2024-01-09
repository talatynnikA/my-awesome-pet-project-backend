# My Awesome Pet Project Backend

This is a Flask-based backend for the My Awesome Pet Project. It provides an API to retrieve information about the developer and contacts.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- [Python](https://www.python.org/) (version 3.6 or higher)
- [PostgreSQL](https://www.postgresql.org/) database

### Installing

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/talatynnikA/my-awesome-pet-project-backend.git
    ```

2. Navigate to the project directory:

    ```bash
    cd my-awesome-pet-project-backend
    ```

3. Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:

    - On Windows:

    ```bash
    venv\Scripts\activate
    ```

    - On macOS/Linux:

    ```bash
    source venv/bin/activate
    ```

5. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

6. Set up environment variables:

   Create a `.env` file in the project root and add the following:

    ```env
    DB_USERNAME=your_postgres_username
    DB_PASSWORD=your_postgres_password
    DB_URI=your_database_name
    ```

7. Apply database migrations:

    ```bash
    flask db upgrade
    ```

### Running the Application

1. Start the Flask application:

    ```bash
    flask run
    ```

2. Open your browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/contacts) to access the API.

### API Endpoints

- `/`: Get information about me.
- `/contacts`: Get contact information.

## Authors

- Artyom Talatynnik


