from django.contrib.messages import success
from django.views.generic.edit import CreateView, UpdateView,  DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AuthorsForm

class BookCreate(CreateView):
    model = Book
    fields = "__all__"
    success_url = reverse_lazy("books")

class BookUpdate(UpdateView):
    model = Book
    fields = "__all__"
    success_url = reverse_lazy("books")

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')

# изменение данных в БД
def edit1(request, id):
    author = Author.objects.get(id=id)
    if request.method == "POST":
        try:
            author.first_name = request.POST.get("first_name")
            author.last_name = request.POST.get("last_name")
            author.date_of_birth = request.POST.get("date_of_birth")
            author.date_of_death = request.POST.get("date_of_death")
            author.save()
            return HttpResponseRedirect("/authors_add/")
        except:
            return HttpResponseNotFound("Не корректные данные ввода даты рождения и смерти.")
    else:
        return render(request, "edit1.html", {"author": author})

# удаление авторов иэ БД
def delete(request, id):
    try:
        author = Author.objects.get(id=id)
        author.delete()
        return HttpResponseRedirect("/authors_add/")
    except Author.DoesNotExist:
        return HttpResponseNotFound("<h2>Aвтop не найден</h2>")

# сохранение данных об авторах в БД
def create(request):
    if request.method == "POST":
        author = Author()
        author.first_name = request.POST.get("first_name")
        author.last_name = request.POST.get("last_name")
        author.date_of_birth = request.POST.get("date_of_birth")
        author.date_of_death = request.POST.get("date_of_death")
        author.save()
        return HttpResponseRedirect("/authors_add/")

# получение данных из БД и загрузка шаблона authors add.html
def authors_add(request):
    author = Author.objects.all()
    authorsform = AuthorsForm()
    return render(request, "catalog/authors_add.html", {"form": authorsform, "author": author})

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='1').order_by('due_back')

class AuthorListViews(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author

class BookDetailView(generic.DetailView):
    model = Book

class BookListViews(generic.ListView):
    model = Book
    paginate_by = 10

    # template_name = 'book_list.html'
    # template_name = 'books.html'

# Create your views here.
def index(request):
    # Генерация некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус= 'На складе')
    # Здесь метод 'all()' применен по умолчанию.
    num_instances_available = BookInstance.objects.filter(status_id=2).count()
    # Авторы книг,
    num_authors = Author.objects.count()
    # Отрисовка НТМL-шаблона index.html с данными
    # внутри переменной context
    # Жанры
    genres = Genre.objects.all()

    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    return render(request, 'index.html',
                  context = {'num_books': num_books,
                             'num_instances': num_instances,
                             'num_instances_available': num_instances_available,
                             'num_authors': num_authors,
                             'genres': genres,
                             'num_visits': num_visits,
                             },
                  )