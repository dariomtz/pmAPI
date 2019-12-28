from django import forms

class NewProject(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField()
    deadline = forms.DateTimeField()

class NewTask(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField()
    deadline = forms.DateTimeField()
    startDate = forms.DateTimeField()
    resources = forms.CharField()

class PutProject(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField()
    deadline = forms.DateTimeField()
    status = forms.BooleanField()

class PatchProject(forms.Form):
    title = forms.CharField(max_length=100, required=False)
    description = forms.CharField(required=False)
    deadline = forms.DateTimeField(required=False)
    status = forms.BooleanField(required=False)

    