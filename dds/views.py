
from .models import CashFlow
from django.shortcuts import render, get_object_or_404


# список записей
def record_list(request):
    return render(request, "record_list.html")


# добавление записи
def record_add(request):
    return render(request, "record_form.html")


# редактирование записи
def record_edit(request, pk=None):
    obj = None
    if pk:
        obj = get_object_or_404(CashFlow, pk=pk)
    return render(request, 'record_form.html', {'object': obj})


# удаление записи
def record_delete(request, pk=None):
    obj = None
    if pk:
        obj = get_object_or_404(CashFlow, pk=pk)
    return render(request, 'record_confirm_delete.html', {'object': obj})
