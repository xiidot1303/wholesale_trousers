from django.shortcuts import render
from django.db.models import Sum
from django.utils.dateparse import parse_date
from app.models import Sale, SaleItem, Store, DailyProductBalance, IncomeItem

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

def daily_report(request):
    date = request.GET.get('date')
    if date:
        product_balances = DailyProductBalance.objects.filter(date=date)
        total_balance = product_balances.aggregate(Sum('quantity'))['quantity__sum'] or 0
        total_income = IncomeItem.objects.filter(income__datetime__date=date).aggregate(Sum('quantity'))['quantity__sum'] or 0
        total_sales = SaleItem.objects.filter(sale__datetime__date=date).aggregate(Sum('quantity'))['quantity__sum'] or 0
        remaining_balance = total_balance + total_income - total_sales

        incomes_by_manufacturer = IncomeItem.objects.filter(income__datetime__date=date).values('product__manufacturer__title').annotate(total_income=Sum('quantity')).order_by('-total_income')
        sales_by_store = SaleItem.objects.filter(sale__datetime__date=date).values('sale__store__title').annotate(total_sales=Sum('quantity')).order_by('-total_sales')
    else:
        total_balance = total_income = total_sales = remaining_balance = 0
        incomes_by_manufacturer = []
        sales_by_store = []

    context = {
        'date': date,
        'total_balance': total_balance,
        'total_income': total_income,
        'total_sales': total_sales,
        'remaining_balance': remaining_balance,
        'incomes_by_manufacturer': incomes_by_manufacturer,
        'sales_by_store': sales_by_store,
    }
    return render(request, 'app/daily_report.html', context)


def redirect_page(request):
    return render(request, 'redirect_page.html')