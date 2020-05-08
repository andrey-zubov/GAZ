from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import (
    LoginForm,
    RegisterForm,
    ContractForm,
    Contract,
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views import View
from datetime import date


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
    template_name = 'contracts/contract_main.html'
    today_year = date.today().year
    titles = []
    finance_costs = []
    activity_forms = []
    curators = []
    contract_type = []
    contract_mode = []
    purchase_type = []
    number_ppz = [] # Номер ППЗ АСЭЗ
    stateASEZ = []
    contract_status = []
    plan_sum_SAP = []
    register_number_SAP = [] # Регистрационный № договора в SAP
    contract_number = []
    fact_sign_date = []
    contract_period = [] # Период действия договора TODO это что?
    counterpart = []
    sum_bez_nds = []# Сумма заключенного договора, всего без НДС
    forecast_total = []
    economy_total = []
    fact_total = []
    economy_total_absolute = []
    total_sum_unsigned_contracts = []
    ecomy_result = []

    def get(self, request):
        contracts = Contract.objects.filter(start_date__contains=self.today_year).order_by('-id')
        form = ContractForm
        return render(request, template_name=self.template_name, context={'form':form,
                                                                          'contracts':contracts,
                                                                        })
