from django import forms
from django.core.exceptions import ValidationError
from app.models import SaleItem, ProductBalance

class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = '__all__'

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        product = self.cleaned_data.get('product')
        
        # Check if the instance already exists (i.e., it's an update)
        if self.instance.pk is None:
            if product:
                product_balance, _ = ProductBalance.objects.get_or_create(product=product)
                if product_balance.quantity < quantity:
                    raise ValidationError(f"Omborda ushbu tovardan yetarlicha mavjuda emas. Qoldiq: {product_balance.quantity}")
    
        return quantity
