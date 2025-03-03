from django.shortcuts import render
from django.db.models import Sum
from django.utils.dateparse import parse_date
from app.models import Sale, SaleItem, Store

def statistics_view(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    sales = Sale.objects.all()
    if start_date:
        sales = sales.filter(datetime__gte=parse_date(start_date))
    if end_date:
        sales = sales.filter(datetime__lte=parse_date(end_date))

    total_sales = sales.count()
    total_revenue = sales.aggregate(Sum('price'))['price__sum'] or 0
    total_products_sold = SaleItem.objects.filter(sale__in=sales).aggregate(Sum('quantity'))['quantity__sum'] or 0

    revenue_by_store = sales.values('store__title').annotate(total_revenue=Sum('price')).order_by('-total_revenue')

    context = {
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        'total_products_sold': total_products_sold,
        'revenue_by_store': revenue_by_store,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'app/statistics.html', context)