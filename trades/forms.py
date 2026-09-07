from django import forms
from .models import Trade

class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = ['entry_symbol', 'entry', 'exit', 'entry_side', 'quantity']
        
    def clean_entry_symbol(self):
        symbol = self.cleaned_data['entry_symbol'].strip().upper()

        if not symbol:
            raise forms.ValidationError("Symbol cannot be empty.")

        return symbol

    def clean_entry(self):
        entry = self.cleaned_data['entry']

        if entry <= 0:
            raise forms.ValidationError("Entry price must be greater than 0.")

        return entry

    def clean_exit(self):
        exit_price = self.cleaned_data['exit']

        if exit_price <= 0:
            raise forms.ValidationError("Exit price must be greater than 0.")

        return exit_price

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']

        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than 0.")

        return quantity