from django import forms


class BaseAPIForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(BaseAPIForm, self).__init__(*args, **kwargs)
