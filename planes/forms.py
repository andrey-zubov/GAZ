from django import forms
from django.forms.widgets import Select
from planes.models import (
  Planning,
  Contract,
  SumsBYN,
  SumsRUR,
  Curator
  )


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class':'sign-in-textfield',
        'placeholder':"Login",
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'sign-in-textfield',
        'placeholder':'Password',
    }))


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField(required=True)


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        exclude = []
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'введите название'})
        }


class SumsRURForm(forms.ModelForm):
    class Meta:
        model = SumsRUR
        exclude = ['contract']


class SumsBYNForm_months(forms.ModelForm): # TODO TESTdelete it away
    class Meta:
        model = SumsBYN
        fields = [
            'period',
            'forecast_total',
            'fact_total',
            ]

class SumsBYNForm_quarts(forms.ModelForm): # TODO TESTdelete it away
    class Meta:
        model = SumsBYN
        fields = [
            'period',
            'plan_sum_SAP',
            'contract_sum_without_NDS_BYN',
        ]


class SumsBYNForm_year(forms.ModelForm):
    class Media:
        js = ('planes/js/script_form_year.js',)

    class Meta:
        model = SumsBYN
        fields = [
            'period',
            'contract_sum_with_NDS_BYN',
            'contract_sum_without_NDS_BYN',
        ]


class PlanningForm(forms.ModelForm):
    curator = forms.ModelChoiceField(Curator.objects.exclude(title='ALL'))
    delete = forms.BooleanField(label='удалить', required=False)

    class Meta:
        model = Planning
        fields = (
            'FinanceCosts', 'curator', 'year',
            'q_1', 'q_2', 'q_3', 
            'q_4', 'delete'
            )
        labels={
            'FinanceCost':'Статья финансирования',
            'curator':'Куратор',
            'year':'Год',
            'q_1':'Квартал 1',
            'q_2':'Квартал 2',
            'q_3':'Квартал 3',
            'q_4':'Квартал 4'
        }

class YearForm(forms.ModelForm):
    class Meta:
        model = Planning
        fields = ('year',)
        labels = {
            'year': 'Год'
        }


class UploadFileForm(forms.Form):
    file = forms.FileField()
