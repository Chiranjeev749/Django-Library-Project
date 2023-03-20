from django.shortcuts import render
from django.http import HttpResponse
from catalog.models import Book,BookInstance,Author,Language,Genre
from django.views.generic import CreateView,DetailView,ListView
from django.urls import reverse_lazy,reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def index(request):
    num_books=Book.objects.all().count()
    num_instance=BookInstance.objects.all().count()
    num_instance_avail=BookInstance.objects.filter(status__exact='a').count()

    context={
        'num_books':num_books,
        'num_instance':num_instance,
        'num_instance_avail':num_instance_avail
    }
    return render(request,'catalog/index.html',context=context)

class BookCreate(LoginRequiredMixin,CreateView):
    model = Book
    fields =  "__all__"
    success_url = reverse_lazy('book_detail')

class BookDetailView(DetailView):
    model = Book

@login_required
def my_view(request):
    return render(request,'catalog/my_view.html')

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'catalog/signup.html'
    success_url =reverse_lazy('login')

class ProfileView(LoginRequiredMixin,ListView):
    model = BookInstance
    template_name="catalog/profile.html"
    paginate_by=5
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user)