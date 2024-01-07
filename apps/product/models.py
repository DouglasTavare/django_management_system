from django.db import models

objects = models.Manager()


class Product(models.Model):
    """
    Model representing a product.

    This model defines the attributes and behavior of a product in the system.

    Attributes:
    - name (str): The name of the product, with a maximum length of 50 characters.
    - description (str): The description of the product, which can be blank or null.
    - price (Decimal): The price of the product, represented as a Decimal with a
                      maximum of 10 digits and 2 decimal places.
    - created_at (DateTime): The date and time when the product was created,
                             automatically set to the current date and time on creation.
    - updated_at (DateTime): The date and time when the product was last updated,
                             automatically updated to the current date and time on each update.

    Methods:
    - __str__(): Returns a string representation of the product with its name,
                 description, and price.
    """

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"Name: {self.name} | Description: {self.description} | Price: {self.price}"
        )
