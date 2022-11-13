from django import forms
from .models import Person,Expenses,Comment
class PersonForm(forms.ModelForm):
    class Meta :
        model=Person
        fields=['name','lastname','week']
        labels={'text':''}
class ExpensesForm(forms.ModelForm):
    class Meta :
        model=Expenses
        fields=['name','cost']
        labels={'text':''}
        widgets={'text':forms.Textarea(attrs={'cols':80})}
class CommentForm(forms.ModelForm):
    class Meta :
        model=Comment
        fields=['name','text']
        labels={'text':''}
        widgets={'text':forms.Textarea(attrs={'cols':80})}