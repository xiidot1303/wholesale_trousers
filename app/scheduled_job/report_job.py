from app.models import *


def create_daily_product_balance():
    product_balances = ProductBalance.objects.all()
    daily_product_balances = [
        DailyProductBalance(
            product=product_balance.product,
            quantity=product_balance.quantity
        )
        for product_balance in product_balances
    ]
    DailyProductBalance.objects.bulk_create(daily_product_balances)