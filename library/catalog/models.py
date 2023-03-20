from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey('Author',on_delete=models.SET_NULL,null=True)
    summary = models.TextField(max_length=600,null=True)
    isbn = models.CharField("ISBN",max_length=13,unique=True)
    genre = models.ManyToManyField(Genre)
    language=models.ForeignKey('Language',on_delete=models.SET_NULL,null=True)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_detail",kwargs={"pk",self})


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50,null=True)
    date_of_birth = models.DateField(null=True,blank=True)

    class Meta:
        ordering =['first_name','last_name']

    def get_absolute_url(self):
        return reverse('author_detail',kwargs={'pk':self.pk})

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

import uuid

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    book = models.ForeignKey('Book',on_delete=models.RESTRICT,null=True)
    imprint = models.CharField(max_length=200)
    due_back=models.DateField(null=True,blank=True)
    borrower = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    
    Loan_Status=(
        ('m','Maintainance'),
        ('o',"On loan"),
        ('a','available'),
        ('r','reservered'),
    )

    status= models.CharField(max_length=1,choices=Loan_Status,blank=True,default='m')

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f"{self.id} {self.book.title}"

