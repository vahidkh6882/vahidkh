from django.shortcuts import render,redirect,get_object_or_404
from .models import Person,Expenses,Comment
from .forms import PersonForm,ExpensesForm,CommentForm
from django.http import Http404
from django.contrib.auth.decorators import login_required
def index(request):
    return render(request,'app1/index.html')
@login_required
def person(request):                                                #persons list with expenses in cartable
    person=Person.objects.filter(captain=request.user)
    comments=Comment.objects.filter(userpage=request.user)
    expenses=Expenses.objects.filter(person=request.user).order_by('date_added')
    s=1
    x=[]
    for i in reversed(expenses):
        x.append(i)
        if(s>=5):
            break
        s=s+1
    content={'person':person,'expenses':x ,'comments':comments}
    return render(request,'app1/person.html',content)
@login_required
def persons_personal(request,topic_id):                                      #page of a person in a captain group 
    person=get_object_or_404(Person,id=topic_id)
    if person.captain != request.user :
        raise Http404
    context={'person':person}
    return render(request,'app1/persons_personal.html',context)
@login_required
def expenses(request):                                                  #page expenses
    expenses=Expenses.objects.filter(person=request.user).order_by('date_added')
    context={'expenses':expenses}
    return render(request,'app1/expenses.html',context)
@login_required
def new_person(request):
    persons=Person.objects.filter(captain=request.user)
    if request.method !='POST' :
        form=PersonForm()
    else:
        form=PersonForm(data=request.POST)
        if form.is_valid():
            new_person=form.save(commit=False)
            new_person.captain=request.user
            new_person.adminswitch=False
            new_person.owe=0
            new_person.bullet=0
            new_person.save()
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
            form.save()
            return redirect('app1:person')
    context={'person':person,'form':form}
    return render(request,'app1/edit_person.html',context)
@login_required
def delete_expenses(request,item_id):
    expenses=Expenses.objects.get(id=item_id)
    expenses.delete()
    return redirect('app1:person')
@login_required
def delete_person(request,item_id):
    person=Person.objects.get(id=item_id)
    if (person.adminswitch == False) :
        person.delete()
    elif(person.adminswitch == True) :
        raise Http404
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
          return redirect('app1:person')
    content={'form':form}
    return render(request,'app1/add_comment.html',content)


     
# Create your views here.
