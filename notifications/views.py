from django.shortcuts import render
from planes.models import Contract

from datetime import date
# import locale

# Create your views here.


def index(request):

    # obj_list = Contract.objects.get(contract_active=True)
    obj_list = Contract.objects.all()
    # obj_list = Contract.objects.all().order_by('title')
    notes_list = []
    today = date.today()

    # задаем локаль для вывода даты на русском языке 'ru'
    # locale.setlocale(locale.LC_ALL, "ru")

    for obj in obj_list:

        if ((obj.plan_load_date_ASEZ - today).days < 30):
            notes_list.append({
                "type": 'plan_load_date_ASEZ',
                "date": obj.plan_load_date_ASEZ.strftime("%d.%m.%Y"),
                "text": 'До загрузки в АСЭЗ договора < ' + obj.title + ' > осталось '+ str((obj.plan_load_date_ASEZ - today).days) + ' дней',
            })

        if ((obj.plan_sign_date - today).days < 30):
            notes_list.append({
                "type": 'plan_sign_date',
                "date": obj.plan_sign_date.strftime("%d.%m.%Y"),
                "text": 'До планируемой даты заключения договора < ' + obj.title + ' > осталось ' + str((obj.plan_sign_date - today).days) + ' дней',
            })

        if (obj.end_time is not None):
            if ((obj.end_time - today).days < 30):
                notes_list.append({
                    "type": 'end_time',
                    "date": obj.end_time.strftime("%d.%m.%Y"),
                    "text": 'Срок действия договора  < ' + obj.title + ' > истекает через ' + str((obj.end_time - today).days) + ' дней',
                })

    context = {'notes_list': notes_list}
    return render(request, 'notifications/index.html', context)
