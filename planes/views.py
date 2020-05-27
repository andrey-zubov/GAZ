from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import (
    LoginForm,
    RegisterForm,
    ContractForm,
    SumsBYNForm,
    SumsRURForm,
    PlanningForm,
    YearForm,
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views import View
from datetime import date
from datetime import datetime as dt
from .models import (
    Contract,
    SumsBYN,
    SumsRUR,
    UserActivityJournal,
    Curator, 
    FinanceCosts, 
    Planning,
)
from django.shortcuts import get_object_or_404
from django.forms import model_to_dict
import json


@login_required
def index(request):
    return render(request, 'planes/index.html')


@login_required
def logout_view(request):
    logout(request)
    return render(request, 'planes/index.html')


def login_view(request,):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    return HttpResponse('disable account')
            else:
                return redirect('/login/')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def register_view(request):
    form = None
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        email = request.POST.get('email')
        username = request.POST.get('username')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким адресом уже существует')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
        else:
            if form.is_valid():
                username = form.cleaned_data['username']
                email = email
                password = User.objects.make_random_password(4)
                user = User.objects.create_user(
                    username,
                    email,
                    password
                )
                user.save()
                create_journal = UserActivityJournal.objects.create(user=user)
                create_journal.save()
                send_mail(
                    'Hello from GAZ',
                    'Ваш пароль: ' + str(password),
                    'gazprombelgaz@gmail.com',
                    [email],
                    fail_silently=False
                )
                return HttpResponse(("Регистрация прошла успешна, пароль отправлен на почту: %s") % str(email))
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)


class ContractView(View):
    ''' render contracts register table and allow to search '''
    template_name = 'contracts/contract_main.html'
    today_year = date.today().year

    def get(self, request):
        contracts = Contract.objects.filter(
            start_date__contains=self.today_year,
            contract_active=True).order_by('-id')
        contract_and_sum = []

        for contract in contracts:
            sums_byn = SumsBYN.objects.filter(contract=contract)
            sum_rur = SumsRUR.objects.get(contract=contract)

            period_byn = {}
            for sum in sums_byn:
                sum_dic = {'plan_sum_SAP':sum.plan_sum_SAP,
                           'contract_sum_without_NDS_BYN':sum.contract_sum_without_NDS_BYN,
                           'forecast_total':sum.forecast_total,
                           'economy_total':sum.economy_total,
                           'fact_total':sum.fact_total,
                           'economy_contract_result':sum.economy_contract_result}

                period_byn[sum.period] = sum_dic

            contract_and_sum.append(
                {
                    'contract':contract,
                    'sum_byn':period_byn,
                    'sum_rur':sum_rur,
                }
            )

        return render(request,
                      template_name=self.template_name,
                      context={'contracts':contracts,
                               'contract_and_sum':contract_and_sum,
                               })


class DeletedContracts(View):
    def get(self, reqest):
        deleted_contracts = Contract.objects.filter(contract_active=False)
        return render(reqest,
                      template_name='contracts/deleted_contracts.html',
                      context={
                          'contracts':deleted_contracts,
                      })

    def post(self, request):
        return HttpResponse('post')


from django.forms import formset_factory, modelformset_factory
def test(request):
    # SumBYNFormSet = formset_factory(SumsBYNForm, extra=0) # создает НОВЫЕ
    contract = Contract.objects.latest('id') # TODO
    SumBYNFormSet = modelformset_factory(SumsBYN, SumsBYNForm, extra=0) # Берет ИЗ БД
    if request.method == "POST":
        formset = SumBYNFormSet(request.POST)
        if formset.is_valid():
            print(formset.cleaned_data)
            contract = Contract.objects.latest('id') # TODO PLACEHOLDER
            for form in formset:
                new_sum_byn = form.save(commit=False)
                new_sum_byn.contract = contract
                new_sum_byn.save()
            return HttpResponse('poset')
        else:
            print(formset.errors)
            return HttpResponse('Невалидненько')

    formset = SumBYNFormSet(queryset=SumsBYN.objects.filter(contract=contract)) # для вызова из бд

    # formset = SumBYNFormSet(initial=[ # для создание нового договора
    #     {'period':'1quart'},
    #     {'period':'2quart'},
    #     {'period':'3quart'},
    #     {'period':'4quart'},
    # ])
    return render(request, template_name='contracts/test.html', context={'formset':formset})


class ContractFabric(View):
    ''' allow to create, change, copy and delete (move to deleted) contracts '''
    create_or_add = 'contracts/add_new_contract.html'

    def get(self, request, contract_id=None):
        if request.GET.__contains__('from_ajax'):
            if request.GET['from_ajax'] == 'del_contract':
                contract_id_list = request.GET.getlist('choosed[]')
                Contract.objects.filter(id__in=contract_id_list).update(contract_active=False)
                return HttpResponse('this is delete contract')

        if request.GET.__contains__('pattern_contract_id'):
            contract_id = int(request.GET['pattern_contract_id'])

        contract_form, sum_byn_forms, sum_rur_form = self.make_forms(request, contract_id)

        return render(request,
                      template_name=self.create_or_add,
                      context={
                          'contract_form': contract_form,
                          'sum_byn_form': sum_byn_forms,
                          'sum_rur_form': sum_rur_form,
                      })

    def post(self, request, contract_id=None):
        contract_form, sum_byn_forms, sum_rur_form = self.make_forms(request, contract_id)

        if contract_form.is_valid() and sum_rur_form.is_valid():
            for byn_form in sum_byn_forms:
                if not byn_form.is_valid():
                    return HttpResponse('форма не валидна')
        else:

            new_contract = contract_form.save()
            for byn_form in sum_byn_forms:
                contract_sum_b = byn_form.save(commit=False)
                contract_sum_b.contract = new_contract
                contract_sum_b.save()
            contract_sum_r = sum_rur_form.save(commit=False)
            contract_sum_r.contract = new_contract
            contract_sum_r.save()
            return HttpResponse('saved')

        return render(request,
                      template_name=self.create_or_add,
                      context={
                          'contract_form': contract_form,
                          'sum_byn_form': sum_byn_forms,
                          'sum_rur_form': sum_rur_form,
                      })

    def make_forms(self, request,  contract_id):
        ''' creates instance objects for forms
        and
        return forms based on instance objects '''
        if not contract_id:
            instance_contract = None
            instance_sum_byn = None
            instance_sum_rur = None
        else:
            instance_contract = get_object_or_404(Contract, id=contract_id)
            instance_sum_rur = get_object_or_404(SumsRUR, contract__id=contract_id)

            qs_sum_byn = SumsBYN.objects.filter(contract__id=contract_id)
            # instance_sum_byn = get_object_or_404(SumsBYN, contract__id=contract_id)

        if request.method == 'POST':
            contract_form = ContractForm(request.POST, instance=instance_contract)
            sum_rur_form = SumsRURForm(request.POST, instance=instance_sum_rur)

            sum_byn_forms = []
            for byn in qs_sum_byn:
                byn_form = SumsRURForm(request.POST, instance=byn)
                sum_byn_forms.append(byn_form)
            # sum_byn_form = SumsBYNForm(request.POST, instance=instance_sum_byn)

        else:
            contract_form = ContractForm(None, instance=instance_contract)
            sum_rur_form = SumsRURForm(None, instance=instance_sum_rur)

            sum_byn_forms = []
            for byn in qs_sum_byn:
                byn_form = SumsRURForm(None, instance=byn)
                sum_byn_forms.append(byn_form)
            # sum_byn_form = SumsBYNForm(None, instance=instance_sum_byn)


        return contract_form, sum_byn_forms, sum_rur_form


def adding_click_to_UserActivityJournal(request):
     counter = UserActivityJournal.objects.get(user=request.user)
     counter.clicks += 1
     counter.save()
     return HttpResponse('add_click')


def plane(request):
    finance_costs = FinanceCosts.objects.all()
    year = YearForm(initial={
        'year': dt.now().year
    })
    
    send_list = []
    money = None
    for item in finance_costs:
        try:
            money = item.with_planning.get(curator__title="ALL")
        except Planning.DoesNotExist:
            plan = Planning()
            plan.FinanceCosts = FinanceCosts.objects.get(pk = item.id)
            plan.curator = Curator.objects.get(title = "ALL")
            plan.q_1 = 0
            plan.q_2 = 0
            plan.q_3 = 0
            plan.q_4 = 0
            plan.year = dt.now().year
            plan.save()
            money = item.with_planning.get(curator__title="ALL")
        send_list.append([item, money])

    response = {"finance_costs": finance_costs,'send_list':send_list, 'year':year}
    return render(request, './planes/plane.html', response)


def curators(request, finance_cost_id):
    planning = Planning.objects.filter(FinanceCosts=finance_cost_id).exclude(curator__title='ALL')
    finance_cost_name = FinanceCosts.objects.get(pk=finance_cost_id).title
    response = {
        'planning': planning,
        'finance_cost_name': finance_cost_name,
        'finance_cost_id':finance_cost_id           
    }
    return render (request, './planes/curators.html', response)

  
def from_js(request):
    a = request.body.decode('utf-8')
    jsn = json.loads(a)
    try:
        result_curator = Curator.objects.get(title='ALL')
        id_result_curator = result_curator.id
    except Curator.DoesNotExist:
        print('error')
        result_curator = Curator()
        result_curator.title = 'ALL'
        result_curator.save()
        id_result_curator = result_curator.id


    finance_cost_title = jsn['cost_title']
    id_finance_cost = FinanceCosts.objects.get(title=finance_cost_title).id

    try:
        planing = Planning.objects.filter(FinanceCosts = id_finance_cost)
        result_cur = planing.get(curator__title='ALL')
    except Planning.DoesNotExist:
        plan = Planning()
        plan.FinanceCosts = FinanceCosts.objects.get(pk = id_finance_cost)
        plan.curator = Curator.objects.get(pk = id_result_curator)
        plan.q_1 = jsn['result_money'][0]
        plan.q_2 = jsn['result_money'][1]
        plan.q_3 = jsn['result_money'][2]
        plan.q_4 = jsn['result_money'][3]
        plan.year = dt.now().year
        plan.save()
        result_cur = planing.get(curator__title='ALL')
    
    if result_cur.q_1 != jsn['result_money'][0] : 
        result_cur.q_1 = jsn['result_money'][0]
    if result_cur.q_2 != jsn['result_money'][1]:
        result_cur.q_2 = jsn['result_money'][1]
    if result_cur.q_3 != jsn['result_money'][2]:
        result_cur.q_3 = jsn['result_money'][2]
    if result_cur.q_4 != jsn['result_money'][3]:
        result_cur.q_4 = jsn['result_money'][3]
    result_cur.save()
    return HttpResponse('123')


def edit_plane(request, item_id):
    plan = Planning.objects.get(pk=item_id)
    plan_form = PlanningForm(instance=plan)
    response = {'plan_form':plan_form, 'item_id':item_id}
    if(request.method == 'POST'):
        plan_form = PlanningForm(request.POST, instance=plan)
        if plan_form.is_valid():
            if plan_form.cleaned_data.get('delete'):
                Planning.objects.get(pk=item_id).delete()
                return redirect(f'/plane/{str(plan.FinanceCosts.id)}/curators' ) 
            plan_form.save()
            return redirect(f'/plane/{str(plan.FinanceCosts.id)}/curators' )
    return render(request, './planes/edit_plane.html', response)

  
def add(request, finance_cost_id):
    plane_form = PlanningForm(initial={
        'FinanceCosts': finance_cost_id,
        'year': dt.now().year,
        })
    response = {
        'plane_form':plane_form,
        'finance_cost_id':finance_cost_id
    }
    if(request.method == 'POST'):
        plane_form = PlanningForm(request.POST)
        if plane_form.is_valid():
            plane_form.save()
            return redirect(f'/plane/{str(finance_cost_id)}/curators' )
    return render(request, './planes/add.html', response)
