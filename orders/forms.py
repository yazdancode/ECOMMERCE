from django import forms


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,  # مقدار حداقل را در خود فرم بررسی کنید
        error_messages={"min_value": "تعداد محصول باید حداقل ۱ باشد."},
    )
