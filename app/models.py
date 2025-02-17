from django.db import models


class Manufacturer(models.Model):
    title = models.CharField(null=True, max_length=64)
    region = models.CharField(null=True, max_length=64)


class Product(models.Model):
    title = models.CharField(null=True, max_length=255)
    manufacturer = models.ForeignKey(Manufacturer, null=True, on_delete=models.PROTECT)
    MEASUREMENT_CHOICES = [
        ("piece", "Dona"),
        ("pack", "Pachka")
    ]
    measurement = models.CharField(null=True, choices=MEASUREMENT_CHOICES, max_length=32, default="pack")
    quantity_in_pack = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title


class Income(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=0)
    datetime = models.DateTimeField(auto_now_add=True, db_index=True)


class ProductBalance(models.Model): # Остаток товаров
    product = models.ForeignKey(Product, null=True, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=0)


class Store(models.Model):
    title = models.CharField(null=True, max_length=64)

    def __str__(self) -> str:
        return self.title


class Client(models.Model):
    name = models.CharField(null=True, max_length=64)
    phone = models.CharField(null=True, max_length=32)


class SaleItem(models.Model):
    sale = models.ForeignKey('app.Sale', null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.PROTECT)
    quantity = models.IntegerField()


class Sale(models.Model):
    store = models.ForeignKey(Store, null=True, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.PROTECT)
    datetime = models.DateTimeField(auto_now_add=True, db_index=True)