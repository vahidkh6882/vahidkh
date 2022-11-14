from django.db import models
from django.contrib.auth.models import User
class Person(models.Model):
  
    captain=models.ForeignKey(User,on_delete=models.CASCADE)
    adminswitch=models.BooleanField(default=False)
    name=models.CharField(max_length=200)
    lastname=models.CharField(max_length=200)
    owe=models.IntegerField()
    bullet=models.IntegerField()
    
    def __str__(self):
        return self.name + " " + self.lastname
class Expenses(models.Model):
    person=models.ForeignKey(User, on_delete = models.CASCADE)
    name=models.TextField()
    cost=models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    class Meta :
        verbose_name_plural='expenses'
    def __str__(self):
        return f"{self.name[:50]}..."
# Create your models here.
class Comment(models.Model):
    userpage=models.ForeignKey(User, on_delete = models.CASCADE)
    name=models.CharField(max_length=200)
    text=models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.text
