from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='expenses'),
    path('add-expenses', views.add_expenses, name='add_expense'),
    path('edit-expense/<int:id>', views.expense_edit, name='edit-expense'),
    path('delete-expense/<int:id>', views.expense_delete, name='delete-expense')
]