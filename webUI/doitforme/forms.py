# Created by SezerBozkir<admin@sezerbozkir.com> at 11/2/2020
from django import forms


from doitforme.models import Servers


class AddServerForm(forms.ModelForm):

    class Meta:
        model = Servers
        exclude = ["owner", "log_data"]
        widgets = {
            'password': forms.PasswordInput(),
        }
