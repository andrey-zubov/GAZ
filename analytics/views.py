from django.shortcuts import render
from .forms import RDKZForm
from planes.models import Contract, Counterpart, PurchaseType, NumberPZTRU, SumsRUR, ContractStatus, ContractRemarks, SumsBYN, Currency

def analytics(request):
    response = {}
    return render(request, './analytics/analytics.html', response)

def report_RKDZ(request):
    if request.method == 'GET':
        form=RDKZForm()
        response = {'form':form}
    form = RDKZForm()
    response = {'form': form}
    return render(request, './analytics/report_RKDZ.html', response)


def report_RKDZ_table(request):
    TABLE_LEGEND={
        "counterpart":"Контрагент",
        "fact_sign_date":"Дата заключения договора",
        "contract_number":"Номер договора",
        "title":"Наименование договора",
        "purchase_type":"Тип закупки",
        "number_ppz":"№ ППЗ",
        "number_PZTRU":"№ пункта Положения о закупках товаров, работ, услуг",
        "contract_sum_NDS_RUB":"Первоначальная цена договора, в рос.руб.",
        "contract_sum_NDS_RUB_sub":"Общая цена договора с учетом всех дополнительных соглашений, рос.руб.",
        "contract_status":"Статус договора",
        "ContractRemarks":"Примечание",
        "subsidiary":"Подразделение",
        "register_number_SAP":"Регистрационный № SAP",
        "start_max_price_ASEZ_NDS":"НМЦ АСЭЗ с НДС, рос.руб.",
        "currency_rate_on_load_date_ASEZ_NDS":"Курс в АСЭЗ",
        "contract_sum_with_NDS_BYN":"Сумма договора в SAP с НДС, бел.руб.",
        "contract_sum_NDS_RUB_2":"Сумма договора, рос.руб.",
        "currency":"Валюта договора"

    }
    CATALOG_FIELDS=[
        "counterpart",
        "purchase_type",
        "number_PZTRU",
        "contract_sum_NDS_RUB",
        "contract_sum_NDS_RUB_sub",
        "contract_status",
        "ContractRemarks",
        "subsidiary",
        "start_max_price_ASEZ_NDS",
        "currency_rate_on_load_date_ASEZ_NDS",
        "contract_sum_with_NDS_BYN",
        "contract_sum_NDS_RUB_2",
        "currency"
    ]
    final_fields=[]
    contracts=Contract.objects.all()
    mystery=[]
    super_list = []
    if request.method=="GET":
        fields=request.GET

        print("Here are field", fields)

        for f in fields.keys():
            final_fields.append((str(TABLE_LEGEND[f]).replace("'","").replace("[","").replace("]",""), f))
            mystery.append(str(f))

    contr_count = 0
    for contr in Contract.objects.filter(contract_active='True').values():
        contr_count += 1
        contr_info=[]
        contr_info.append(contr_count)
        for mir in mystery:
            for key in contr.keys():
                if mir in key:
                    if mir in CATALOG_FIELDS:
                        if mir == 'counterpart':
                            try:
                                contr_info.append(Counterpart.objects.filter(id=contr[key]).values('name')[0]['name'])
                            except:
                                contr_info.append('-')
                        elif mir == 'purchase_type':
                            try:
                                contr_info.append(PurchaseType.objects.filter(id=contr[key]).values('title')[0]['title'])
                            except:
                                contr_info.append('-')
                        elif mir == "number_PZTRU":
                            try:
                                contr_info.append(NumberPZTRU.objects.filter(id=contr[key]).values('title')[0]['title'])
                            except:
                                contr_info.append('-')
                        elif mir == "contract_status":
                            try:
                                contr_info.append(ContractStatus.objects.filter(id=contr[key]).values('title')[0]['title'])
                            except:
                                contr_info.append('-')
                    else:
                        contr_info.append(contr[key])

            if mir == "contract_sum_NDS_RUB":
                try:
                    contr_info.append(SumsRUR.objects.filter(contract__id=contr['id'], year='2020').values(
                        'contract_sum_NDS_RUB')[0]['contract_sum_NDS_RUB'])
                except:
                    contr_info.append('-')
            elif mir == "contract_sum_NDS_RUB_sub":
                number_ppz = contr['number_ppz']
                try:
                    contr_info.append(SumsRUR.objects.filter(contract__number_ppz=number_ppz, year='2020').aggregate(sum=Sum('contract_sum_NDS_RUB'))['sum'])
                except:
                    contr_info.append('-')
            elif mir == "ContractRemarks":
                try:
                    contr_info.append(ContractRemarks.objects.filter(contract__id=contr['id']).values(
                        'remark_text')[0]['remark_text'])
                except:
                    contr_info.append('-')
            elif mir == "subsidiary":
                contr_info.append("Филиал Минское УМГ")
            elif mir == "start_max_price_ASEZ_NDS":
                try:
                    contr_info.append(SumsRUR.objects.filter(contract__id=contr['id'], year='2020').values(
                        'start_max_price_ASEZ_NDS')[0]['start_max_price_ASEZ_NDS'])
                except:
                    contr_info.append('-')
            elif mir == "currency_rate_on_load_date_ASEZ_NDS":
                try:
                    contr_info.append(SumsRUR.objects.filter(contract__id=contr['id'], year='2020').values(
                        'currency_rate_on_load_date_ASEZ_NDS')[0]['currency_rate_on_load_date_ASEZ_NDS'])
                except:
                    contr_info.append('-')
            elif mir == "contract_sum_with_NDS_BYN":
                try:
                    contr_info.append(SumsBYN.objects.filter(contract__id=contr['id'], year='2020').values(
                        'contract_sum_with_NDS_BYN')[0]['contract_sum_with_NDS_BYN'])
                except:
                    contr_info.append('-')
            elif mir == "contract_sum_NDS_RUB_2":
                try:
                    contr_info.append(SumsRUR.objects.filter(contract__id=contr['id'], year='2020').values(
                        'contract_sum_NDS_RUB')[0]['contract_sum_NDS_RUB'])
                except:
                    contr_info.append('-')
            elif mir == "currency":

                try:
                    cur = SumsRUR.objects.filter(contract__id=contr['id'], year='2020').values(
                        'currency')[0]['currency']
                    contr_info.append(Currency.objects.filter(id=cur).values(
                        'title')[0]['title'])
                except:
                    contr_info.append('-')

        super_list.append(contr_info)

    for item in super_list:
        for each in item:
            if not each:
                a = item.index(each)
                b = super_list.index(item)
                super_list[b][a] = "-"


    print("А теперь чудо", super_list)
    # print("Чудесный список", mystery)

    response = {
        "final_fields":final_fields,
        "len":range(1, (len(final_fields) + 2)),
        "contracts":contracts,
        "mystery":mystery,
        "super_list":super_list
        }
    return render(request, './analytics/report_RKDZ_table.html', response)

