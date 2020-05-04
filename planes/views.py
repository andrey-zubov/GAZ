from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .models import FinanceCosts, Planning
from datetime import datetime

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
    return render(request, template_name='registration/login.html', context={'form': form})


@login_required
def planing_finance_costs(request):\
    # здесь будут суммы поквартально и итог
    # здесь будет выбор года отображения
    plans = Planning.objects.all()
    this_year = datetime.today()
    filtered_plans = Planning.objects.filter(year=this_year)
    return render(request,
                  template_name='planes/fin_costs.html',
                  context={'plans':plans,
                           'this_year':this_year,
                           'filtered_plans':filtered_plans,
                           })
