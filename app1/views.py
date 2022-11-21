from django.shortcuts import render,redirect,get_object_or_404
from .models import Person,Expenses,Comment,Ip
from .forms import PersonForm,ExpensesForm,CommentForm
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from django.db.models import Q
def index(request):
    def get_ip(request):
        address = request.META.get('HTTP_X_FORWARDED_FOR')
        if address :
            ip = address.split(',')[-1].strip()
        else : 
            ip = request.META.get('REMOTE_ADDR')
        return ip
    ip = get_ip(request)
    u = Ip(ip=ip)
    result = Ip.objects.filter(Q(ip__icontains=ip))
    if len(result) == 1:
        print("user exist")
    elif len(result) > 1 :
        print("user exist more ...")
    else : 
        u.save()
        print("user is unique")
    count = Ip.objects.all().count()
    print("total user is ",count)
    context = {'count':count}
    return render(request,'app1/index.html',context)
@login_required
def person(request):                                                #persons list with expenses in cartable
    CHOICES={'5':'saturday','6':'sunday','0':'monday','1':'tuesday','2':'wednesday','3':'thursday','4':'friday'}
    person=Person.objects.filter(captain=request.user)
    comments=Comment.objects.filter(userpage=request.user)
    expenses=Expenses.objects.filter(person=request.user).order_by('date_added')
    dt = datetime.now()
    day=dt.weekday()
    duty_owner = 'null'
    for person_duty in person:
        if person_duty.week == str(day) :
            duty_owner = person_duty.name + " " + person_duty.lastname + " : today ( " + CHOICES[person_duty.week] + " )"
            break
    s=1
    x=[]
    for i in reversed(expenses):
        x.append(i)
        if(s>=5):
            break
        s=s+1
    content={'person':person,'expenses':x ,'comments':comments,'duty_owner':duty_owner}
    return render(request,'app1/person.html',content)
@login_required
def persons_personal(request,topic_id):                                      #page of a person in a captain group 
    person=get_object_or_404(Person,id=topic_id)
    weeks={'5':'saturday','6':'sunday','0':'monday','1':'tuesday','2':'wednesday','3':'thursday','4':'friday'}
    duty=weeks[person.week]
    if person.captain != request.user :
        raise Http404
    context={'person':person,'duty':duty}
    return render(request,'app1/persons_personal.html',context)
@login_required
def expenses(request):                                                  #page expenses
    expenses = Expenses.objects.filter(person=request.user).order_by('date_added')
    context={'expenses':expenses}
    return render(request,'app1/expenses.html',context)
@login_required
def new_person(request):
    persons=Person.objects.filter(captain=request.user)
    if request.method != 'POST' :
        form=PersonForm()
    else:
        form=PersonForm(data=request.POST)
        if form.is_valid():
            new_person=form.save(commit=False)
            for x in persons : 
                if new_person.week == x.week:
                    raise Http404
            new_person.captain=request.user
            new_person.adminswitch=False
            new_person.owe=0
            new_person.bullet=0
            new_person.save()
            messages.success(request, "The person has been successfully added . ")
            return redirect('app1:person')
    context={'form':form}
    return render(request,'app1/new_person.html',context)
@login_required
def new_expenses(request):
    expenses=Expenses.objects.filter(person=request.user).order_by('date_added')
    persons=Person.objects.filter(captain=request.user)
    number=Person.objects.filter(captain=request.user).count()
    if request.method !='POST':
          form=ExpensesForm()
    else:
        form=ExpensesForm(data=request.POST)
        if form.is_valid():
            new_entry =form.save(commit=False)
            costp = new_entry.cost / number
            new_entry.person=request.user
            for person in persons :
                if costp <= person.bullet :
                    person.bullet -= costp
                elif costp > person.bullet :
                    x= costp - person.bullet
                    person.bullet=0
                    person.owe+=x
                person.save()
            new_entry.save()
            messages.success(request, "The item has been successfully added . ")
            return redirect('app1:person')
    context={'expenses':expenses,'form':form}
    return render(request,'app1/new_expenses.html',context)
@login_required
def edit_expenses(request,entry_id):
    persons=Person.objects.filter(captain=request.user)
    expenses=Expenses.objects.get(id=entry_id)
    number=Person.objects.filter(captain=request.user).count()
    if request.method != 'POST' :
        form = ExpensesForm(instance=expenses)
    else:
        costfirst= expenses.cost / number
        form=ExpensesForm(instance=expenses,data=request.POST)
        if form.is_valid():
            formx=form.save(commit=False)
            cost_per_person = formx.cost / number           #hazine jadid bara har nafar
            print(costfirst,cost_per_person)
            if cost_per_person  > costfirst :               #age hazine afzayesh yaft
                costbetween = cost_per_person - costfirst         #ekhtelaf bein hazine ghabli va hazine jadid
                for person in persons :
                    if costbetween <= person.bullet :          #age mojoodi dasht
                        person.bullet = person.bullet - costbetween 
                    elif costbetween > person.bullet :        #age mojoodi nakafi bood
                        x= costbetween - person.bullet
                        person.bullet=0
                        person.owe = person.owe + x
                    person.save()
            elif cost_per_person  < costfirst :              #age hazine kam shod
                costbetween = costfirst - cost_per_person     #ekhtelaf bein hazine ghabli va hazine jadid         
                for person in persons :
                    if (person.owe > 0)and((costbetween-person.owe) >= 0) :   #age bedehkar bood va va ba mohasebat be bullet ham ezafe beshe
                        person.bullet = person.bullet + (costbetween-person.owe) #yani faghat az bedehi kam beshe va be bullet ezafe beshe
                        person.owe=0
                    elif person.owe == 0 :              #age bedehkar nabood be bulletesh ezafe beshe
                        person.bullet = person.bullet + costbetween
                    elif (person.owe > 0)and((person.owe-costbetween)>0) :   #age bedehkar bood kheili faghat bedehi kam beshe
                        person.owe = person.owe - costbetween
                    person.save()
            form.save()
            messages.success(request, "The item has been successfully updated . ")
            return redirect('app1:expenses')
    context={'expenses':expenses,'form':form}
    return render(request,'app1/edit_expenses.html',context)
@login_required
def edit_person_bullet(request,entry_id) :
    person=Person.objects.get(id=entry_id)
    if request.method == 'POST' :
            x=int(request.POST['num'])
            if (person.owe > 0) and (person.owe - x >= 0) :
                person.owe -= x
            elif (person.owe > 0) and (x-person.owe > 0) :
                person.bullet = person.bullet + (x - person.owe)
                person.owe=0
            elif person.owe == 0 :
                person.bullet += x
            person.save()
            messages.success(request, "The person's bullet has been successfully updated . ")
            return redirect('app1:person')
    context={'person':person}
    return render(request,'app1/edit_person_bullet.html',context)
@login_required
def edit_person(request,entry_id):
    persons=Person.objects.filter(captain=request.user)
    person=Person.objects.get(id=entry_id)
    if request.method != 'POST' :
        form=PersonForm(instance=person)
    else :
        form=PersonForm(instance=person,data=request.POST)
        if form.is_valid():
            editperson=form.save(commit=False)
            for x in persons : 
                if editperson.week == x.week:
                    raise Http404
            form.save()
            messages.success(request, "The person has been successfully updated . ")
            return redirect('app1:person')
    context={'person':person,'form':form}
    return render(request,'app1/edit_person.html',context)
@login_required
def delete_expenses(request,item_id):
    expenses=Expenses.objects.get(id=item_id)
    expenses.delete()
    messages.success(request, "The item has been successfully deleted !")
    return redirect('app1:person')
@login_required
def delete_person(request,item_id):
    person=Person.objects.get(id=item_id)
    if (person.adminswitch == False) :
        person.delete()
    elif(person.adminswitch == True) :
        raise Http404
    messages.success(request, "The person has been successfully deleted !")
    return redirect('app1:person')
@login_required
def add_comment(request):
    if request.method != 'POST' :
       form=CommentForm()
    else :
       form=CommentForm(data=request.POST) 
       if form.is_valid() :
          comment=form.save(commit=False)
          comment.userpage=request.user
          comment.save()
          messages.success(request, "Your comment sent seccessfully . ")
          return redirect('app1:person')
    content={'form':form}
    return render(request,'app1/add_comment.html',content)


     
# Create your views here.
