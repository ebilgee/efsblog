from django.utils import timezone
from .models import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerSerializer



def home(request):
   return render(request, 'portfolio/home.html',
                 {'portfolio': home})


@login_required
def customer_list(request):
   customer = Customer.objects.filter(created_date__lte=timezone.now())
   return render(request, 'portfolio/customer_list.html',
                 {'customers': customer})


@login_required
def customer_edit(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   if request.method == "POST":
       # update
       form = CustomerForm(request.POST, instance=customer)
       if form.is_valid():
           customer = form.save(commit=False)
           customer.updated_date = timezone.now()
           customer.save()
           customer = Customer.objects.filter(created_date__lte=timezone.now())
           return render(request, 'portfolio/customer_list.html',
                         {'customers': customer})
   else:
       # edit
       form = CustomerForm(instance=customer)
   return render(request, 'portfolio/customer_edit.html', {'form': form})


@login_required
def customer_delete(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   customer.delete()
   return redirect('portfolio:customer_list')


@login_required
def stock_list(request):
   stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
   return render(request, 'portfolio/stock_list.html', {'stocks': stocks})


@login_required
def stock_new(request):
   if request.method == "POST":
       form = StockForm(request.POST)
       if form.is_valid():
           stock = form.save(commit=False)
           stock.created_date = timezone.now()
           stock.save()
           stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
           return render(request, 'portfolio/stock_list.html',
                         {'stocks': stocks})
   else:
       form = StockForm()
       # print("Else")
   return render(request, 'portfolio/stock_new.html', {'form': form})


@login_required
def stock_edit(request, pk):
   stock = get_object_or_404(Stock, pk=pk)
   if request.method == "POST":
       form = StockForm(request.POST, instance=stock)
       if form.is_valid():
           stock = form.save()
           # stock.customer = stock.id
           stock.updated_date = timezone.now()
           stock.save()
           stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
           return render(request, 'portfolio/stock_list.html', {'stocks': stocks})
   else:
       # print("else")
       form = StockForm(instance=stock)
   return render(request, 'portfolio/stock_edit.html', {'form': form})


@login_required
def stock_delete(request, pk):
   stock = get_object_or_404(Stock, pk=pk)
   stock.delete()
   stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
   return render(request, 'portfolio/stock_list.html', {'stocks': stocks})


@login_required
def investment_list(request):
   investments = Investment.objects.filter(acquired_date__lte=timezone.now())
   return render(request, 'portfolio/investment_list.html', {'investments': investments})

@login_required
def investment_add(request):
   if request.method == "POST":
       form = InvestmentForm(request.POST)
       if form.is_valid():
           investment = form.save(commit=False)
           investment.created_date = timezone.now()
           investment.save()
           investments = Investment.objects.filter(acquired_date__lte=timezone.now())
           return render(request, 'portfolio/investment_list.html',
                         {'investments': investments})
   else:
       form = InvestmentForm()
       # print("Else")
   return render(request, 'portfolio/investment_add.html', {'form': form})

@login_required
def investment_edit(request, pk):
   investment = get_object_or_404(Investment, pk=pk)
   if request.method == "POST":
       form = InvestmentForm(request.POST, instance=investment)
       if form.is_valid():
           investment = form.save()
           investment.updated_date = timezone.now()
           investment.save()
           investments = Investment.objects.filter(acquired_date__lte=timezone.now())
           return render(request, 'portfolio/investment_list.html', {'investments': investments})
   else:
       # print("else")
       form = InvestmentForm(instance=investment)
   return render(request, 'portfolio/investment_edit.html', {'form': form})

@login_required
def investment_delete(request, pk):
    investment = get_object_or_404(Investment, pk=pk)
    investment.delete()
    investments = Investment.objects.filter(acquired_date__lte=timezone.now())
    return render(request, 'portfolio/investment_list.html', {'investments': investments})

@login_required
def portfolio(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customers = Customer.objects.filter(created_date__lte=timezone.now())
    investments = Investment.objects.filter(customer=pk)
    stocks = Stock.objects.filter(customer=pk)
    sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))
    sum_recent_value = Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))

    dcurrencies = Digitalcurrency.objects.filter(customer=pk)


    # Initialize the value of the stocks
    sum_current_stocks_value = 0
    sum_of_initial_stock_value = 0

    sum_current_balance_value = 0
    sum_initial_balance_value = 0

    # Loop through each stock and add the value to the total
    for stock in stocks:
        sum_current_stocks_value += stock.current_stock_value()
        sum_of_initial_stock_value += stock.initial_stock_value()

    for dcurrency in dcurrencies:
        sum_current_balance_value += dcurrency.current_balance_value()
        sum_initial_balance_value += dcurrency.initial_balance_value()

    return render(request, 'portfolio/portfolio.html', {'customers': customers, 'investments': investments,
                                                        'stocks': stocks,
                                                        'dcurrencies' : dcurrencies,
                                                        'sum_current_balance_value' : sum_current_balance_value,
                                                        'sum_initial_balance_value' : sum_initial_balance_value,
                                                        'sum_acquired_value': sum_acquired_value,
                                                        'sum_recent_value': sum_recent_value,
                                                        'sum_current_stocks_value': sum_current_stocks_value,
                                                        'sum_of_initial_stock_value': sum_of_initial_stock_value})



class CustomerList(APIView):
    def get(self,request):
        customers_json = Customer.objects.all()
        serializer = CustomerSerializer(customers_json, many=True)
        return Response(serializer.data)

@login_required
def currency_list(request):
   dcurrencies = Digitalcurrency.objects.filter(purchase_date__lte=timezone.now())
   return render(request, 'portfolio/currency_list.html', {'dcurrencies': dcurrencies})


@login_required
def currency_new(request):
   if request.method == "POST":
       form = CurrencyForm(request.POST)
       if form.is_valid():
           dcurrency = form.save(commit=False)
           dcurrency.created_date = timezone.now()
           dcurrency.save()
           dcurrencies = Digitalcurrency.objects.filter(purchase_date__lte=timezone.now())
           return render(request, 'portfolio/currency_list.html',
                         {'dcurrencies': dcurrencies})
   else:
       form = CurrencyForm()
       # print("Else")
   return render(request, 'portfolio/currency_new.html', {'form': form})


@login_required
def currency_edit(request, pk):
    dcurrency = get_object_or_404(Digitalcurrency, pk=pk)
    if request.method == "POST":
       form = CurrencyForm(request.POST, instance=dcurrency)
       if form.is_valid():
           dcurrency = form.save()
           dcurrency.updated_date = timezone.now()
           dcurrency.save()
           dcurrencies = Digitalcurrency.objects.filter(purchase_date__lte=timezone.now())
           return render(request, 'portfolio/currency_list.html', {'dcurrencies': dcurrencies})
    else:
       # print("else")
       form = CurrencyForm(instance=dcurrency)
    return render(request, 'portfolio/currency_edit.html', {'form': form})


@login_required
def currency_delete(request, pk):
   dcurrency = get_object_or_404(Digitalcurrency, pk=pk)
   dcurrency.delete()
   dcurrencies = Digitalcurrency.objects.filter(purchase_date__lte=timezone.now())
   return render(request, 'portfolio/currency_list.html', {'dcurrencies': dcurrencies})