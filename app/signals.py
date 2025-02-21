from django.dispatch import Signal
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Income, ProductBalance, SaleItem

# Define a custom signal
my_custom_signal = Signal()

# Signal receiver function
def my_signal_receiver(sender, **kwargs):
    print(f"Signal received from {sender}")
    print(f"Arguments: {kwargs}")

# Connect the signal to the receiver
my_custom_signal.connect(my_signal_receiver)

# Signal receiver for updating ProductBalance when Income is created
@receiver(post_save, sender=Income)
def update_product_balance_on_income(sender, instance, created, **kwargs):
    if created:
        product_balance, _ = ProductBalance.objects.get_or_create(product=instance.product)
        product_balance.quantity += instance.quantity
        product_balance.save()

# Signal receiver for updating ProductBalance when SaleItem is created
@receiver(post_save, sender=SaleItem)
def update_product_balance_on_sale(sender, instance, created, **kwargs):
    if created:
        product_balance = ProductBalance.objects.get_or_create(product=instance.product)
        product_balance.quantity -= instance.quantity
        product_balance.save()