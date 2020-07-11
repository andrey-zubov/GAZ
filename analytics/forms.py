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


