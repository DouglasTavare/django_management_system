"""
This test module includes unit tests for the product API in a Django application.

The tests cover the following scenarios:
1. Creating a product with valid data.
2. Creating a product with missing fields (name and price).
3. Creating a product with invalid values (short name, short description, low price).
4. Retrieving product details and a list of products.
5. Attempting to retrieve a product that doesn't exist.
6. Updating a product with valid data using PATCH and PUT methods.
7. Updating a product that doesn't exist.
8. Updating a product with invalid values (short name, short description, low price).
9. Deleting an existing product.
10. Attempting to delete a product that doesn't exist.

The test cases utilize the pytest-django framework, and each test function is marked with 
@pytest.mark.django_db
to ensure the database is set up correctly for testing. The authenticated_api_client fixture is used
to simulate an authenticated API client for making requests.

Note: The database transactions are rolled back at the end of each test to maintain a clean state.

"""
import pytest


@pytest.mark.django_db
def test_create_product(authenticated_api_client) -> None:
    """
    Test the create product API with valid data.

    :param authenticated_api_client: Authenticated API client fixture.
    :return: None
    """
    payload = {
        "name": "Test product",
        "description": "Test product description",
        "price": 650,
    }

    response_create = authenticated_api_client.post(
        "/products/", data=payload, format="json"
    )
    product_id = response_create.data["id"]
    assert response_create.status_code == 201
    assert response_create.data["name"] == payload["name"]

    response_read = authenticated_api_client.get(
        f"/products/{product_id}", format="json"
    )
    assert response_read.status_code == 200
    assert response_read.data["name"] == payload["name"]


@pytest.mark.django_db
def test_create_product_missing_fields(authenticated_api_client) -> None:
    """
    Test the create product API with missing fields (name and price).

    :param authenticated_api_client: Authenticated API client fixture.
    :return: None
    """
    payload = {
        "name": "Test product",
        "description": "Test product description",
        "price": 700,
    }

    del payload["price"]
    response_create = authenticated_api_client.post(
        "/products/", data=payload, format="json"
    )
    assert response_create.status_code == 400
    assert response_create.data["price"] == ["This field is required."]

    del payload["name"]
    response_create = authenticated_api_client.post(
        "/products/", data=payload, format="json"
    )
    assert response_create.status_code == 400
    assert response_create.data["name"] == ["This field is required."]


@pytest.mark.django_db
def test_create_product_with_invalid_values(authenticated_api_client) -> None:
    """
    Test the create product API with invalid values (short name, short description, low price).

    :param authenticated_api_client: Authenticated API client fixture.
    :return: None
    """
    default_payload = {
        "name": "Test product",
        "description": "Test product description",
        "price": 650,
    }

    # Create a product with invalid value for name field (name must have at least 3 characters)
    payload = default_payload
    payload["name"] = "ab"
    response_create = authenticated_api_client.post(
        "/products/", data=payload, format="json"
    )
    assert response_create.status_code == 400
    assert (
        response_create.data["name"][0].title()
        == "Field 'Name' Must Have At Least 3 Characters"
    )

    # Create a product with invalid value for description (name must have at least 10 characters)
    payload = default_payload
    payload["description"] = "descrip"
    response_create = authenticated_api_client.post(
        "/products/", data=payload, format="json"
    )
    assert response_create.status_code == 400
    assert (
        response_create.data["description"][0].title()
        == "Field 'Description' Must Have At Least 10 Characters"
    )

    # Create a product with invalid value for price field (price must be at least 500)
    payload = default_payload
    payload["price"] = 499
    response_create = authenticated_api_client.post(
        "/products/", data=payload, format="json"
    )
    assert response_create.status_code == 400
    assert (
        response_create.data["price"][0].title()
        == "Field 'Price' Must Be Higher Than 500"
    )


@pytest.mark.django_db
def test_get_product(authenticated_api_client) -> None:
    """
    Test retrieving product details and a list of products.

    :param authenticated_api_client: Authenticated API client fixture.
    :return: None
    """
    payload = {
        "name": "First test product",
        "description": "Fist test product description",
        "price": 650,
    }

    # Create a product
    response_create = authenticated_api_client.post(
        "/products/", data=payload, format="json"
    )
    assert response_create.status_code == 201
    assert response_create.data["name"] == payload["name"]

    payload = {
        "name": "Second test product",
        "description": "Second test product description",
        "price": 750,
    }

    # Create a product
    response_create = authenticated_api_client.post(
        "/products/", data=payload, format="json"
    )
    product_id = response_create.data["id"]
    assert response_create.status_code == 201
    assert response_create.data["name"] == payload["name"]

    # Read the product data
    response_read = authenticated_api_client.get(
        f"/products/{product_id}", format="json"
    )
    assert response_read.status_code == 200
    assert response_read.data["name"] == payload["name"]

    response_read = authenticated_api_client.get("/products/", format="json")
    assert response_read.status_code == 200
    assert len(response_read.data["results"]) == 2


@pytest.mark.django_db
def test_get_product_that_doesnt_exist(authenticated_api_client) -> None:
    """
    Test retrieving product details and a list of products.

    :param authenticated_api_client: Authenticated API client fixture.
    :return: None
    """
    response_read = authenticated_api_client.get("/products/1", format="json")
    assert response_read.status_code == 404
    assert response_read.data["detail"] == "Not found."


@pytest.mark.django_db
def test_patch_product(authenticated_api_client) -> None:
    """
    Test updating a product with valid data using the PATCH method.

    :param authenticated_api_client: Authenticated API client fixture.
    :return: None
    """
    payload = {
        "name": "Test product",
        "description": "Test product description",
        "price": 650,
    }

    # Create a product
    response_create = authenticated_api_client.post(
        "/products/", data=payload, format="json"
    )
    product_id = response_create.data["id"]
    assert response_create.status_code == 201
    assert response_create.data["name"] == payload["name"]

    # Update the product
    response_update = authenticated_api_client.patch(
        f"/products/{product_id}", data={"name": "Test product"}, format="json"
    )
    assert response_update.status_code == 200
    assert response_update.data["name"] == payload["name"]


@pytest.mark.django_db
def test_patch_product_that_doesnt_exist(authenticated_api_client) -> None:
    """
    Test updating a product that doesn't exist with the PATCH method.

    :param authenticated_api_client: Authenticated API client fixture.
    :return: None
    """
    response_update = authenticated_api_client.patch(
        "/products/1", data={"name": "Test product"}, format="json"
    )
    assert response_update.status_code == 404
    assert response_update.data["detail"] == "Not found."


@pytest.mark.django_db
def test_patch_product_with_invalid_values(authenticated_api_client) -> None:
    """
    Test updating a product with invalid values (short name, short description, low price) using
    the PATCH method.

    :param authenticated_api_client: Authenticated API client fixture.
    :return: None
    """
    payload = {
        "name": "Test product",
        "description": "Test product description",
        "price": 650,
    }

    # Create a product
    response_create = authenticated_api_client.post(
        "/products/", data=payload, format="json"
    )
    product_id = response_create.data["id"]
    assert response_create.status_code == 201
    assert response_create.data["name"] == payload["name"]

    response_update = authenticated_api_client.patch(
        f"/products/{product_id}", data={"name": "ab"}, format="json"
    )
    assert response_update.status_code == 400
    assert (
        response_update.data["name"][0].title()
        == "Field 'Name' Must Have At Least 3 Characters"
    )

    # Create a product with invalid value for description (name must have at least 10 characters)
    response_update = authenticated_api_client.patch(
        f"/products/{product_id}", data={"description": "ab"}, format="json"
    )
    assert response_update.status_code == 400
    assert (
        response_update.data["description"][0].title()
        == "Field 'Description' Must Have At Least 10 Characters"
    )

    # Create a product with invalid value for price field (price must be at least 500)
    response_update = authenticated_api_client.patch(
        f"/products/{product_id}", data={"price": 5}, format="json"
    )
    assert response_update.status_code == 400
    assert (
        response_update.data["price"][0].title()
        == "Field 'Price' Must Be Higher Than 500"
    )


@pytest.mark.django_db
def test_put_product(authenticated_api_client) -> None:
    """
    Test updating a product with valid data using the PUT method.

    :param authenticated_api_client: Authenticated API client fixture.
    :return: None
    """
    payload = {
        "name": "Test product",
        "description": "Test product description",
        "price": 650,
    }

    # Create a product
    response_create = authenticated_api_client.post(
        "/products/", data=payload, format="json"
    )
    product_id = response_create.data["id"]
    assert response_create.status_code == 201
    assert response_create.data["name"] == payload["name"]

    # Update the product
    payload["name"] = "Updated test product"
    response_update = authenticated_api_client.put(
        f"/products/{product_id}", data=payload, format="json"
    )
    assert response_update.status_code == 200
    assert response_update.data["name"] == payload["name"]


@pytest.mark.django_db
def test_put_product_that_doesnt_exist(authenticated_api_client) -> None:
    """
    Test updating a product that doesn't exist with the PUT method.

    :param authenticated_api_client: Authenticated API client fixture.
    :return: None
    """
    update_payload = {
        "name": "Updated product name",
        "description": "Updated product description",
        "price": 700,
    }

    response_update = authenticated_api_client.patch(
        "/products/1", data=update_payload, format="json"
    )
    assert response_update.status_code == 404
    assert response_update.data["detail"] == "Not found."


@pytest.mark.django_db
def test_put_product_with_invalid_values(authenticated_api_client) -> None:
    """
    Test updating a product with invalid values (short name, short description, low price) using
    the PUT method.

    :param authenticated_api_client: Authenticated API client fixture.
    :return: None
    """
    payload = {
        "name": "Test product",
        "description": "Test product description",
        "price": 650,
    }

    # Create a product
    response_create = authenticated_api_client.post(
        "/products/", data=payload, format="json"
    )
    product_id = response_create.data["id"]
    assert response_create.status_code == 201
    assert response_create.data["name"] == payload["name"]

    # Update the product
    payload["name"] = "ab"
    response_update = authenticated_api_client.put(
        f"/products/{product_id}", data=payload, format="json"
    )
    assert response_update.status_code == 400
    assert response_update.data["name"] == [
        "Field 'name' must have at least 3 characters"
    ]

    # Update the product
    payload["description"] = "ab"
    response_update = authenticated_api_client.put(
        f"/products/{product_id}", data=payload, format="json"
    )
    assert response_update.status_code == 400
    assert response_update.data["description"] == [
        "Field 'description' must have at least 10 characters"
    ]

    # Update the product
    payload["price"] = 400
    response_update = authenticated_api_client.put(
        f"/products/{product_id}", data=payload, format="json"
    )
    assert response_update.status_code == 400
    assert response_update.data["price"] == ["Field 'price' must be higher than 500"]


@pytest.mark.django_db
def test_delete_product(authenticated_api_client) -> None:
    """
    Test deleting an existing product.

    :param authenticated_api_client: Authenticated API client fixture.
    :return: None
    """
    payload = {
        "name": "Test product",
        "description": "Test product description",
        "price": 650,
    }

    # Create a product
    response_create = authenticated_api_client.post(
        "/products/", data=payload, format="json"
    )
    product_id = response_create.data["id"]
    assert response_create.status_code == 201
    assert response_create.data["name"] == payload["name"]

    # Delete the product
    response_delete = authenticated_api_client.delete(
        f"/products/{product_id}", format="json"
    )
    assert response_delete.status_code == 204

    # Read the product
    response_read = authenticated_api_client.get(
        f"/products/{product_id}", format="json"
    )
    assert response_read.status_code == 404

    # product doesn't exist
    response_delete = authenticated_api_client.delete(
        f"/products/{product_id + 1}", format="json"
    )
    assert response_delete.status_code == 404


@pytest.mark.django_db
def test_delete_product_that_doesnt_exist(authenticated_api_client) -> None:
    """
    Test attempting to delete a product that doesn't exist.

    :param authenticated_api_client: Authenticated API client fixture.
    :return: None
    """
    response_delete = authenticated_api_client.delete("/products/1", format="json")
    assert response_delete.status_code == 404
