from django import forms

class NewProject(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField()
    deadline = forms.DateTimeField(required=False) 

class NewTask(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField()
    deadline = forms.DateTimeField(required=False)
    startDate = forms.DateTimeField(required=False)
    resources = forms.CharField(required=False)

class PutProject(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField()
    deadline = forms.DateTimeField()
    status = forms.NullBooleanField()
    
    def clean_status(self):
        data = self.cleaned_data['status']
        if data == None:
            raise forms.ValidationError('Enter a valid boolean value.', code='invalid')
        return data

class PatchProject(forms.Form):
    title = forms.CharField(max_length=100, required=False)
    description = forms.CharField(required=False)
    deadline = forms.DateTimeField(required=False)
    status = forms.NullBooleanField(required=False)

    