from django.shortcuts import render,redirect
from django.contrib.auth import login
from app1.forms import PersonForm
from app1.models import Person
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
def register(request):
    if request.method != 'POST':
        form=UserCreationForm()
    else:
        form=UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user=form.save()
            login(request,new_user)
            form2=Person()
            form2.name=new_user.username
            form2.captain=request.user
            form2.lastname="(admin)"
            form2.adminswitch=True
            form2.owe=0
            form2.bullet=0
            form2.save()
            return redirect('app1:index')
    context={'form':form}
    return render(request,'registration/register.html',context)
# Create your views here.
