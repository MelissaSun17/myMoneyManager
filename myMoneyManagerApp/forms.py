import datetime

from django import forms
from myMoneyManagerApp.models import Transaction, Budget


class TransactionForm(forms.ModelForm):
    category_type_choices = (
        (1, 'groceries'),
        (2, 'charity'),
        (3, 'eating out'),
        (4, 'entertainment'),
        (5, 'general'),
        (6, 'transport'),
        (7, 'other')
    )

    category = forms.ChoiceField(widget=forms.Select(), choices=category_type_choices, initial=category_type_choices[1])
    description = forms.CharField(help_text="Description:", max_length=32, required=False)
    values = forms.FloatField(help_text="Amount:")
    ownerId = forms.CharField(widget=forms.HiddenInput(), required=False,max_length=255)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Transaction
        fields = ('category', 'description', 'values', 'ownerId')


class BudgetForm(forms.ModelForm):
    ownerId = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    setBudget = forms.FloatField(help_text="Amount:")

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Budget
        fields = ('ownerId', 'setBudget')

