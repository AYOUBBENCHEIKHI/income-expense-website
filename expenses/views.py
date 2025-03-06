from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required 
from .models import Category , Expense
from django.contrib import messages
from django.core.paginator import Paginator

import json
from django.http import JsonResponse
# Create your views here. 

def search_expenses(request):
    if request.method ==   'POST':
        search_str = json.loads(request.body).get('searchText') 
        expenses = Expense.objects.filter(owner=request.user,amount__istartswith=search_str)|Expense.objects.filter(
            owner=request.user,date__istartswith=search_str)|Expense.objects.filter(
                owner=request.user,description__icontains=search_str)|Expense.objects.filter(
                owner=request.user,category__icontains=search_str)
        
        data = expenses.values()
        return JsonResponse(list(data),safe=False)
@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'expenses': expenses,
        'page_obj':page_obj
    }
    return render(request, 'expenses/index.html', context)

def add_expenses(request):
    categories = Category.objects.all()
    context = {
                'categories': categories,
                'values':request.POST
               }
    if request.method =='GET':
        return render(request, 'expenses/add_expenses.html', context)
    if request.method == 'POST':    
        amount = request.POST['amount']
        if not amount : 
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expenses.html', context) 
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['expense_date']
        if not description : 
            messages.error(request, 'description is required')
            return render(request, 'expenses/add_expenses.html', context)
        Expense.objects.create(amount=amount, date=date  ,description=description,owner=request.user, category=category)
        messages.success(request, 'Expense saved successfully')
        return redirect( 'expenses')

def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories,
     }
    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        if not amount : 
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expenses.html', context) 
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['expense_date']
        if not description : 
            messages.error(request, 'description is required')
            return render(request, 'expenses/edit-expenses.html', context)
        expense.amount=amount 
        expense.date=date  
        expense.description=description
        expense.owner=request.user
        expense.category=category
        expense.save()
        messages.success(request, 'Expense Updated successfully')
        return redirect( 'expenses')

def expense_delete(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense deleted successfully')
    return redirect( 'expenses')

    
