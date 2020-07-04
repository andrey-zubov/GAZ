from django import forms
from django.forms.widgets import CheckboxInput

class RDKZForm(forms.Form):

    counterpart = forms.BooleanField(
        label='Контрагент',
        # help_text='Контрагент введите',
        widget=CheckboxInput,
        required=False
    )

    fact_sign_date = forms.BooleanField(
        label='Дата заключения договора',
        widget=CheckboxInput,
        required=False
    )

    contract_number = forms.BooleanField(
        label='Номер договора',
        widget=CheckboxInput,
        required=False
    )

    title = forms.BooleanField(
        label='Наименование договора',
        widget=CheckboxInput,
        required=False
    )

    purchase_type = forms.BooleanField(
        label='Тип закупки',
        widget=CheckboxInput,
        required=False
    )

    number_ppz = forms.BooleanField(
        label='№ ППЗ',
        widget=CheckboxInput,
        required=False
    )

    number_PZTRU = forms.BooleanField(
        label='№ пункта Положения о закупках товаров, работ, услуг',
        widget=CheckboxInput,
        required=False
    )

    contract_sum_NDS_RUB = forms.BooleanField(
        label='Первоначальная цена договора, в рос.руб.',
        widget=CheckboxInput,
        required=False
    )

    contract_sum_NDS_RUB_sub = forms.BooleanField(
        label='Общая цена договора с учетом всех дополнительных соглашений, рос.руб.',
        widget=CheckboxInput,
        required=False
    )

    contract_status = forms.BooleanField(
        label='Статус договора',
        widget=CheckboxInput,
        required=False
    )

    ContractRemarks = forms.BooleanField(
        label='Примечание',
        widget=CheckboxInput,
        required=False
    )

    subsidiary = forms.BooleanField(
        label='Подразделение',
        widget=CheckboxInput,
        required=False
    )

    register_number_SAP = forms.BooleanField(
        label='Регистрационный № SAP',
        widget=CheckboxInput,
        required=False
    )

    start_max_price_ASEZ_NDS = forms.BooleanField(
        label='НМЦ АСЭЗ с НДС, рос.руб.',
        widget=CheckboxInput,
        required=False
    )

    currency_rate_on_load_date_ASEZ_NDS = forms.BooleanField(
        label='Курс в АСЭЗ',
        widget=CheckboxInput,
        required=False
    )

    contract_sum_with_NDS_BYN = forms.BooleanField(
        label='Сумма договора в SAP с НДС, бел.руб.',
        widget=CheckboxInput,
        required=False
    )

    contract_sum_NDS_RUB_2 = forms.BooleanField(
        label='Сумма договора, рос.руб.',
        widget=CheckboxInput,
        required=False
    )

    currency = forms.BooleanField(
        label='Валюта договора',
        widget=CheckboxInput,
        required=False
    )







