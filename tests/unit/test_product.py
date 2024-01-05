from django.test import TestCase
from django.urls import reverse
import pytest

"""
The following annotation ensures the database is set up correctly for testing.
Each test will run in its own transaction, which will be rolled back at the end of the test.
"""

@pytest.mark.django_db
def test_create_product(authenticated_api_client) -> None:  
    """  
    Test the create product API  
    :param api_client:  
    :return: None  
    """  
    payload = {
        "name": "Test product",
        "description": "Test product description",
        "price": 650
    }

    # Create a product  
    response_create = authenticated_api_client.post("/products/", data=payload, format="json")  
    product_id = response_create.data["id"]  
    assert response_create.status_code == 201  
    assert response_create.data["name"] == payload["name"]  
  
    # Read the product data
    response_read = authenticated_api_client.get(f"/products/{product_id}", format="json")  
    assert response_read.status_code == 200  
    assert response_read.data["name"] == payload["name"]

@pytest.mark.django_db  
def test_create_product_with_invalid_data(authenticated_api_client) -> None:
    """  
    Test the create product API  
    :param api_client:  
    :return: None  
    """  
    default_payload = {
        "name": "Test product",
        "description": "Test product description",
        "price": 650
    }
  
    # Create a product with invalid value for name field (name must have at least 3 characters)
    payload = default_payload
    payload['name'] = 'ab'
    response_create = authenticated_api_client.post("/products/", data=payload, format="json")  
    assert response_create.status_code == 400 
    assert response_create.data["name"][0].title() == "Field 'Name' Must Have At Least 3 Characters"
    

    # Create a product with invalid value for description field (name must have at least 10 characters)
    payload = default_payload
    payload['description'] = 'descrip'
    response_create = authenticated_api_client.post("/products/", data=payload, format="json")  
    assert response_create.status_code == 400 
    assert response_create.data["description"][0].title() == "Field 'Description' Must Have At Least 10 Characters"
  
    # Create a product with invalid value for price field (price must be at least 500)
    payload = default_payload
    payload['price'] = 499
    response_create = authenticated_api_client.post("/products/", data=payload, format="json")  
    assert response_create.status_code == 400 
    assert response_create.data["price"][0].title() == "Field 'Price' Must Be Higher Than 500"

@pytest.mark.django_db  
def test_get_product(authenticated_api_client) -> None:
    """  
    Test the update product API  
    :param api_client:  
    :return: None  
    """  
    payload = {
        "name": "First test product",
        "description": "Fist test product description",
        "price": 650
    }
  
    # Create a product  
    response_create = authenticated_api_client.post("/products/", data=payload, format="json")  
    assert response_create.status_code == 201  
    assert response_create.data["name"] == payload["name"] 

    payload = {
        "name": "Second test product",
        "description": "Second test product description",
        "price": 750
    }
  
    # Create a product  
    response_create = authenticated_api_client.post("/products/", data=payload, format="json")
    product_id = response_create.data["id"]  
    assert response_create.status_code == 201  
    assert response_create.data["name"] == payload["name"]

    # Read the product data
    response_read = authenticated_api_client.get(f"/products/{product_id}", format="json")  
    assert response_read.status_code == 200  
    assert response_read.data["name"] == payload["name"]

    response_read = authenticated_api_client.get(f"/products/", format="json")  
    assert response_read.status_code == 200  
    assert len(response_read.data["results"]) == 2

@pytest.mark.django_db  
def test_patch_product(authenticated_api_client) -> None:  
    """  
    Test the update product API  
    :param api_client:  
    :return: None  
    """  
    payload = {
        "name": "Test product",
        "description": "Test product description",
        "price": 650
    }
  
    # Create a product  
    response_create = authenticated_api_client.post("/products/", data=payload, format="json")  
    product_id = response_create.data["id"]  
    assert response_create.status_code == 201  
    assert response_create.data["name"] == payload["name"] 

    # Update the product  
    response_update = authenticated_api_client.patch(  
        f"/products/{product_id}", data={"name": "Test product"}, format="json"  
    )  
    assert response_update.status_code == 200
    assert response_update.data["name"] == payload["name"]
  
    # Product doesn't exist  
    response_update = authenticated_api_client.patch(  
        f"/products/{product_id + 1}", data=payload, format="json"  
    )  
    assert response_update.status_code == 404

@pytest.mark.django_db  
def test_put_product(authenticated_api_client) -> None:  
    """  
    Test the update product API  
    :param api_client:  
    :return: None  
    """  
    payload = {
        "name": "Test product",
        "description": "Test product description",
        "price": 650
    }
  
    # Create a product  
    response_create = authenticated_api_client.post("/products/", data=payload, format="json")  
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
  
    # Product doesn't exist  
    response_update = authenticated_api_client.put(  
        f"/products/{product_id + 1}", data=payload, format="json"  
    )  
    assert response_update.status_code == 404

@pytest.mark.django_db  
def test_delete_product(authenticated_api_client) -> None:  
    """  
    Test the delete product API  
    :param api_client:  
    :return: None  
    """  
    payload = {
        "name": "Test product",
        "description": "Test product description",
        "price": 650
    }  
  
    # Create a product  
    response_create = authenticated_api_client.post("/products/", data=payload, format="json")  
    product_id = response_create.data["id"]  
    assert response_create.status_code == 201  
    assert response_create.data["name"] == payload["name"] 
  
    # Delete the product  
    response_delete = authenticated_api_client.delete(f"/products/{product_id}", format="json")  
    assert response_delete.status_code == 204  
  
    # Read the product  
    response_read = authenticated_api_client.get(f"/products/{product_id}", format="json")  
    assert response_read.status_code == 404  
  
    # product doesn't exist  
    response_delete = authenticated_api_client.delete(f"/products/{product_id + 1}", format="json")  
    assert response_delete.status_code == 404