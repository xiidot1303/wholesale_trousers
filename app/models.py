from django.db import models


class Manufacturer(models.Model):
    title = models.CharField(null=True, max_length=64, verbose_name="Brend nomi")
    region = models.CharField(null=True, max_length=64, verbose_name="Hudud")

    class Meta:
        verbose_name = "Ishlab chiqaruvchi"
        verbose_name_plural = "Ishlab chiqaruvchilar"


class Product(models.Model):
    title = models.CharField(null=True, max_length=255, verbose_name="Mahsulot nomi")
    manufacturer = models.ForeignKey(Manufacturer, null=True, on_delete=models.PROTECT, verbose_name="Ishlab chiqaruvchi")
    MEASUREMENT_CHOICES = [
        ("piece", "Dona"),
        ("pack", "Pachka")
    ]
    measurement = models.CharField(null=True, choices=MEASUREMENT_CHOICES, max_length=32, 
        default="pack", verbose_name="O'lchov birligi")
    quantity_in_pack = models.IntegerField(null=True, blank=True, verbose_name="Pachkadagi miqdor")

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"

    def __str__(self) -> str:
        return self.title


class Income(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.PROTECT, verbose_name="Mahsulot")
    quantity = models.IntegerField(default=0, verbose_name="Miqdori")
    datetime = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Vaqt")

    class Meta:
        verbose_name = "Kirim"
        verbose_name_plural = "Kirimlar"


class ProductBalance(models.Model): # Остаток товаров
    product = models.ForeignKey(Product, null=True, on_delete=models.PROTECT, verbose_name="Mahsulot")
    quantity = models.IntegerField(default=0, verbose_name="Miqdori")

    class Meta:
        verbose_name = "Ombor"
        verbose_name_plural = "Ombor"


class Store(models.Model):
    title = models.CharField(null=True, max_length=64, verbose_name="Do'kon nomi")

    class Meta:
        verbose_name = "Do'kon"
        verbose_name_plural = "Do'konlar"

    def __str__(self) -> str:
        return self.title


class Client(models.Model):
    name = models.CharField(null=True, max_length=64, verbose_name="Mijoz ismi")
    phone = models.CharField(null=True, max_length=32, verbose_name="Telefon raqami")

    class Meta:
        verbose_name = "Mijoz"
        verbose_name_plural = "Mijozlar"


class SaleItem(models.Model):
    sale = models.ForeignKey('app.Sale', null=True, on_delete=models.CASCADE, verbose_name="Savdo")
    product = models.ForeignKey(Product, null=True, on_delete=models.PROTECT, verbose_name="Mahsulot")
    quantity = models.IntegerField(verbose_name="Miqdor")

    class Meta:
        verbose_name = "Savdo mahsuloti"
        verbose_name_plural = "Savdo mahsulotlari"


class Sale(models.Model):
    store = models.ForeignKey(Store, null=True, on_delete=models.PROTECT, verbose_name="Do'kon")
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.PROTECT, verbose_name="Mijoz")
    datetime = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Vaqt")

    class Meta:
        verbose_name = "Savdo"
        verbose_name_plural = "Savdolar"
