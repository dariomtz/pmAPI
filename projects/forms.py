from django import forms

class NewProject(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField()
    deadline = forms.DateTimeField()

class PutProject(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField()
    deadline = forms.DateTimeField()

class NewTask(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField()
    deadline = forms.DateTimeField()
    startDate = forms.DateTimeField()
    resources = forms.CharField()

    