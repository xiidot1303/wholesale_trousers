from app.views import *
from app.models import Archive
from django.shortcuts import redirect
from django.db.models import F


class ArchiveProductView(CreateView):
    model = Archive
    fields = ['product', 'quantity']
    success_url = '/admin/app/archive'
    template_name = 'admin/app/archive/change_list.html'
    

    def form_valid(self, form):
        product = form.cleaned_data['product']
        quantity = form.cleaned_data['quantity']
        type = self.request.POST.get('type')
        
        # Check if an Archive object with the same product already exists
        existing_archive = Archive.objects.filter(product=product).first()
        
        if existing_archive:
            # find product balance and minus quantity from their
            product_balance = ProductBalance.objects.filter(product=product).first()
            if product_balance:
                if type == 'add':
                    product_balance.quantity -= quantity
                    existing_archive.quantity += quantity
                else:
                    product_balance.quantity += quantity
                    existing_archive.quantity -= quantity
                # if quantity of the product balance is less than 0, return error
                if product_balance.quantity < 0:
                    messages.error(self.request, 'Omborda yetarli miqdorda mahsulot yo\'q')
                    return redirect_back(self.request)
                if existing_archive.quantity < 0:
                    messages.error(self.request, 'Arxivda yetarli miqdorda mahsulot yo\'q')
                    return redirect_back(self.request)
                product_balance.save()
            # If it exists, update the quantity
            existing_archive.save()
            return redirect(self.success_url)
        else:
            # If it doesn't exist, create a new Archive object
            return super().form_valid(form)

