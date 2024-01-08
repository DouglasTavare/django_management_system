# Django Management System

##### The following application consists of a product system management composed of a REST API that enables its operations to be done, as well as a SQLite database instance for the data managed through the API to be persisted and consumed.


### Model Definition:
The current project has its model definition described below:
- id (Auto-generated primary key)
- name (String, required, minimum length: 3 characteres)
- description (Text, optional, minimum length: 10 characteres)
- price (Decimal, required, minimum value: 500)
- created_at (DateTime, auto-set on creation)
- updated_at (DateTime, auto-update on modification)

### Setup

In order to set up the application the user has to start the virtual environment through **pipenv** library resource.

First make sure you have **pip** installed. With that being said, in order to install **pipenv** dependency management library, run the following command:

```bash
pip install pipenv
```

After that, inside the root directory, run the following command in order to install the dependencies required to run the project:
```bash
pipenv install
```

After the required dependencies being installed, it's time to start up the virtual environment used for this project. That can be done by running the following command:
```bash
pipenv shell
```

Now the virtual environment is up and properly recognizing the project's dependencies. With that, the Management System project can be executed through the following command run inside the root directory:
```bash
pipenv run python manage.py runserver
```

After that, the project is running on **http://localhost:8000/**.

### Authentication
To start using the management system, the system user has to create a Django admin user, this can be done by running the following command: 
```bash
pipenv run python manage.py createsuperuser
```

After that it's required to fill the shown fields with admin user information (Username, Email address and Password).

With the admin user created, the system user has to authenticate its information with the JWT Token Authentication method. This can be done by running a POST method this the admin user information, to the authentication endpoint, as demonstrated below:

#### Get token
```bash
POST /token/

{
    "username":"admin_user",
    "password":"admin_user_password"
}
```

This request will return a **refresh** and **access** objects, the **access** one will be used in the API methods requests, and the **refresh** one will be used in order to refresh the generated token when it expires.
This **access** token will expire in 10 minutes, and can be retrieved by running the following request:

#### Refresh token
```bash
POST /token/refresh/

{
    "refresh":"token_refresh_value"
}
```

### API Methods
In order to properly access the API methods, the user has to pass the generated JWT Token as a Bearer token in the requests tool used for it. With that, the following requests can be done in order to access and interact with the API:

##### POST product
```bash
POST /products/

{
    "name": {product_name},
    "description": {product_description},
    "price": {product_price}
}
```

#### GET methods
In order to give control to the user when receiving and pagination the results, for all the GET requests, the query params **page_size** and **page** can be passed in the URL as exampled below:
```bash
GET /products/?page_size={page_size}&page={page}
```

Other query params can be added by simply appending **&** character and the query param followed by its value in the sequence.

##### GET all products
```bash
GET /products/
```

##### GET product by id
```bash
GET /products/{id}
```

##### GET product by name
```bash
GET /products/?name={name}
```

##### GET product by price range
```bash
GET /products/?min_price={min_price}&max_price={max_price}
```
This request can be run passing on one of the price range value if desired (for exemple, only passing min_price but not max_price).

##### PATCH product
```bash
PATCH /products/{id}

{
    "name": {updated_product_name},
}
```
PATCH method updates one, some, but not all fields at a time, so this request can vary by defining other fields values on the payload instead of the one shown.

##### PUT product
```bash
PUT /products/{id}

{
    "name": {updated_product_name},
    "description": {updated_product_description},
    "price": {updated_product_price}
}
```
PUT method requires all the fields to be passed as the payload in order to update the object.

##### DELETE product
```bash
DELETE /products/{id}
```

### Tests
In order to execute the tests written for the REST API functionalities, the following command can be run:

```bash
pipenv run pytest .
```

### Code Quality
In order to verify the quality of the written code, the Pylint linter library can be run, and a summary of the code analysis seen.
```bash
pipenv run pylint *
```

### Code Formatting
In order to verify the formatting pattern of the written code, the Black formatting library can be run, and misformatted files seen.
```bash
pipenv run black . --check
```

### Libraries importing order
In order to verify if the libraries imports are respecting the pattern order, Isort importing order library can be run.
```bash
pipenv run isort . --check-only --profile black
```

### Security validation
In order to guarantee that there is no existing security issues in the code, Bandit security verification library can be run and unsafe files reported.
```bash
pipenv run bandit .
```

### Dependencies vulnerabilities
In order to guarantee that none of the used dependencies have vulnerabilities issues, Safety dependencies verification library can be run, and existing dependencies vulnerabilites get shown.
```bash
pipenv run safety check
```

### CI/CD Pipelines
Code quality and testing pipelines have been created for this current repository, and can be accessed through the GitHub Actions tab within this repository.

### Documentation
Project documentation can be accessed through: [Django Management System Documentation](https://django-management-system.readthedocs.io/en/latest/)
