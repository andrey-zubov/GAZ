from django import forms
from django.forms.widgets import Select
from planes.models import (
  Planning,
  Contract,
  SumsBYN,
  SumsRUR)





class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField(required=True)


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        exclude = []


# class SumsBYNForm(forms.ModelForm):
#     class Meta:
#         model = SumsBYN
#         exclude = ['contract']


class SumsRURForm(forms.ModelForm):
    class Meta:
        model = SumsRUR
        exclude = ['contract']


class SumsBYNForm(forms.ModelForm): # TODO placeholder delet it away
    class Meta:
        model = SumsBYN
        fields = [
            'period',
            'plan_sum_SAP',
            'contract_sum_without_NDS_BYN',
            'forecast_total',
            'fact_total']

# from django.forms import formset_factory
# SumsBYNFormSet = formset_factory(SumsBYNForm)


class PlanningForm(forms.ModelForm):
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
