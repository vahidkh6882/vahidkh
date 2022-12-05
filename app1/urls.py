from django.urls import path
from . import views
from django.contrib import admin
app_name='app1'
urlpatterns=[
    path('',views.index,name='index'),
    path('cartable/',views.person,name='person'),
    path('cartable/<int:topic_id>/',views.persons_personal,name='persons'),
    path('new_person/',views.new_person,name='new_person'),
    path('expenses/',views.expenses,name='expenses'),
    path('new_expenses/',views.new_expenses,name='new_expenses'),
    path('add_comment/',views.add_comment,name='comment'),
    path('edit_person_bullet/<int:entry_id>/',views.edit_person_bullet,name='edit_person_bullet'),
    path('edit_expenses/<int:entry_id>/',views.edit_expenses,name='edit_expenses'),
    path('delete_person/<int:item_id>',views.delete_person,name='delete_person'),
    path('delete_expenses/<int:item_id>',views.delete_expenses,name='delete_expenses'),
    path('edit_person/<int:entry_id>/',views.edit_person,name='edit_person'),
    path('admin/',admin.site.urls,name='admin'),
    ]