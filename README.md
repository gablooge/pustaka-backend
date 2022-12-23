## PUSTAKA

## Run locally

### using docker
- build and run the docker for the production

    ``` bash
    # run database
    docker-compose -f docker-compose.dev.yaml up db -d --build
    # run apps
    docker-compose -f docker-compose.dev.yaml up apps -d --build
    ```

- Open the `http://localhost:9090/admin`

- unit test
    ```
    docker-compose -f docker-compose.dev.yaml up test --build
    ```

### run on host machine
- Once defined (by any convenient means), install the projects requirements via virtualenv,

    ``` bash
    # From project root directory
    python3 -m venv venv
    source ./venv/bin/activate

    # Install base requirements
    pip install -r requirements/base.txt
    pip install -r requirements/dev.txt
    ```

- Run Local

    ```bash
    # export the variables for database if using external database
    export DEBUG=true
    export SECRET_KEY=django-insecure-79gfkx
    export DB_USER=pustaka_user
    export DB_NAME=pustaka_db
    export DB_PASSWORD=11ecb9090242ac111ecb9090242ac
    export DB_HOST=localhost
    export DB_PORT=5432

    python manage.py runserver
    ```

- Database Migrations
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

- Lint Testing
    For lint testing run the following command in the project root

    ```bash
    flake8
    ```

- Unit Test

    For unit testing run the following command in the project root

    ```bash
    python manage.py test --settings=pustaka.settings_local
    ```

- Available commands
    - Generate librarian user
        ```
        python manage.py generate_librarian_user
        ```
