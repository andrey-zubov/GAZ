from planes.models import (
    SumsBYN,
    Contract,
    Planning,
    Curator,
    FinanceCosts,
    ContractType,
    ContractStatus
)
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.db.models import Avg, Count, Min, Sum, Q

def get_analytics_for_all_contracts(request):
    YEARS = [
        2018, 2019, 2020, 2021, 2022, 2023, 2024
    ]
    curators = Curator.objects.all()
    finance_costs = FinanceCosts.objects.all()
    contracts = Contract.objects.all()
    contract_types = ContractType.objects.all()
    contract_status = ContractStatus.objects.all()

    year = '2020'
    curator_id = 1
    finance_cost_id = 1
    contract_type_id = '1'
    contract_status_id = '0'

    if request.GET:
        year = request.GET['select_year']
        curator_id = request.GET['select_curator']
        finance_cost_id = request.GET['select_cost']
        contract_type_id = request.GET['select_contractType']
        contract_status_id = request.GET['select_contractStatus']

    finance_cost_title = FinanceCosts.objects.filter(id=finance_cost_id).values('title')[0]['title']
    curator_title = Curator.objects.filter(id=curator_id).values('title')[0]['title']

    if contract_type_id == '0':
        contract_types_ids = [value['id'] for value in contract_types.values('id')]
    else:
        contract_types_ids = list(contract_type_id)


    status_id = int(contract_status_id)

    contract_status_ids=['0']

    if contract_status_id == '0':
        contract_status_ids = [value['id'] for value in contract_status.values('id')]

    elif contract_status.values('id', 'title').filter(id=status_id)[0]['title']=='Заключен':
        ad =[i['id']  for i in contract_status.values('id', 'title') if i['title'] == 'Исполнен']
        contract_status_ids = list(contract_status_id) + ad

    elif contract_status.values('id', 'title').filter(id=status_id)[0]['title']=='Исполнен':
        ad =[i['id']  for i in contract_status.values('id', 'title') if i['title'] == 'Заключен']
        contract_status_ids = list(contract_status_id) + ad
    else:
        contract_status_ids = list(contract_status_id)

    planning = Planning.objects.filter(
        FinanceCosts_id = finance_cost_id,
        curator_id = curator_id,
        year = year
    ).values()

    if not planning:
        a = Planning(year=year, FinanceCosts_id=finance_cost_id, curator_id=curator_id)
        planning = [a]

    plan_sum_sap_dict = {}
    for period in ['1quart', '2quart', '3quart', '4quart', '6months', '9months', 'year']:
        plan_sum_sap_all = SumsBYN.objects.filter(
        period=period,
        year=year,
        contract__finance_cost_id = finance_cost_id,
        contract__curator_id = curator_id,
        contract__contract_type_id__in=contract_types_ids,

        contract__contract_status_id__in=contract_status_ids,
        contract__contract_active='True'

    ).aggregate(sum = Sum('plan_sum_SAP'))['sum']
        if not plan_sum_sap_all:
            plan_sum_sap_all='0'
        plan_sum_sap_dict[period] = plan_sum_sap_all

    contract_sum_without_NDS_BYN_dict = {}
    for period in ['1quart', '2quart', '3quart', '4quart', '6months', '9months', 'year']:
        contract_sum_without_NDS_BYN_all = SumsBYN.objects.filter(
            period=period,
            year=year,
            contract__finance_cost_id=finance_cost_id,
            contract__curator_id=curator_id,
            contract__contract_type_id__in=contract_types_ids,

            contract__contract_status_id__in=contract_status_ids,
            contract__contract_active='True'
        ).aggregate(sum=Sum('contract_sum_without_NDS_BYN'))['sum']
        if not contract_sum_without_NDS_BYN_all:
            contract_sum_without_NDS_BYN_all='0'
        contract_sum_without_NDS_BYN_dict[period] = contract_sum_without_NDS_BYN_all

    forecast_total_dict = {}
    for period in ['1quart', '2quart', '3quart', '4quart', '6months', '9months', 'year']:
        forecast_total_all = SumsBYN.objects.filter(
            period=period,
            year=year,
            contract__finance_cost_id=finance_cost_id,
            contract__curator_id=curator_id,
            contract__contract_type_id__in=contract_types_ids,

            contract__contract_status_id__in=contract_status_ids,
            contract__contract_active='True'

        ).aggregate(sum=Sum('forecast_total'))['sum']
        if not forecast_total_all:
            forecast_total_all='0'
        forecast_total_dict[period] = forecast_total_all

    fact_total_dict = {}
    for period in ['1quart', '2quart', '3quart', '4quart', '6months', '9months', 'year']:
        fact_total_all = SumsBYN.objects.filter(
            period=period,
            year=year,
            contract__finance_cost_id=finance_cost_id,
            contract__curator_id=curator_id,
            contract__contract_type_id__in=contract_types_ids,
            contract__contract_status_id__in=contract_status_ids,
            contract__contract_active='True'

        ).aggregate(sum=Sum('fact_total'))['sum']
        if not fact_total_all:
            fact_total_all='0'
        fact_total_dict[period] = fact_total_all


    contracts_count_plan = {}

    contracts_count_plan['Все'] = contracts.filter(
        finance_cost_id=finance_cost_id,
        curator_id=curator_id,

        contract_status__title__in=['Запланирован'],
        contract_active='True'


    ).count()

    contracts_count_plan['Центр'] = contracts.filter(
        finance_cost_id=finance_cost_id,
        curator_id=curator_id,
        contract_type__title__in=['Центр'],

        contract_status__title__in=['Запланирован'],
        contract_active = 'True'

    ).count()

    contracts_count_plan['Филиал'] = contracts.filter(
        finance_cost_id=finance_cost_id,
        curator_id=curator_id,
        contract_type__title__in=['Филиал'],

        contract_status__title__in=['Запланирован'],
        contract_active='True'

    ).count()

    contracts_count_fact = {}

    contracts_count_fact['Все'] = contracts.filter(
        finance_cost_id=finance_cost_id,
        curator_id=curator_id,

        contract_status__title__in=['Заключен', 'Исполнен'],
        contract_active='True'

    ).count()

    contracts_count_fact['Центр'] = contracts.filter(
        finance_cost_id=finance_cost_id,
        curator_id=curator_id,
        contract_type__title__in=['Центр'],

        contract_status__title__in=['Заключен', 'Исполнен'],
        contract_active='True'

    ).count()

    contracts_count_fact['Филиал'] = contracts.filter(
        finance_cost_id=finance_cost_id,
        curator_id=curator_id,
        contract_type__title__in=['Филиал'],

        contract_status__title__in=['Заключен', 'Исполнен'],
        contract_active='True'

    ).count()

    return render(request,
                  template_name = "analytics/implementation_plan.html",
                  context = {
                      'curators':curators,
                      'FinanceCosts':finance_costs,
                      'contracts':contracts,
                      'contract_types': contract_types,
                      'contract_status': contract_status,
                      'planning': planning,
                      'years': YEARS,
                      'plan_sum_sap': plan_sum_sap_dict,
                      'contract_sum_without_NDS_BYN':contract_sum_without_NDS_BYN_dict,
                      'plannings': planning[0],
                      'forecast_total': forecast_total_dict,
                      'fact_total': fact_total_dict,
                      'contracts_count_plan': contracts_count_plan,
                      'contracts_count_fact': contracts_count_fact,
                      'year': year,
                      'finance_cost_title': finance_cost_title,
                      'curator_title':curator_title
                      })

