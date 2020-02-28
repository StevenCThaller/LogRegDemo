from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.


def index(request):
    # if 'user_id' in request.session:
    #     return redirect('/success')
    return render(request, 'index.html')


def register(request):
    errors = User.objects.reg_val(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(
        ), bcrypt.gensalt()).decode()  # to encode the password from the form

        new_user = User.objects.create(
            f_name=request.POST['f_name'], l_name=request.POST['l_name'], email=request.POST['email'], password=hashed_pw)
        request.session['user_id'] = new_user.id
        return redirect('/books')


def login(request):
    errors = User.objects.log_val(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            return redirect('/')
    else:
        existing = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = existing.id
        return redirect('/books')


def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return render(request, 'success.html')


def logout(request):
    request.session.clear()
    return redirect('/')


def all_books(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'logged_user': User.objects.get(id=request.session['user_id']),
        'all_books': Book.objects.all()
    }
    return render(request, 'books.html', context)


def add_book(request):
    if 'user_id' not in request.session:
        return redirect('/')
    errors = Book.objects.book_val(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/books')
    logged_in = User.objects.get(id=request.session['user_id'])
    new_book = Book.objects.create(
        title=request.POST['title'], description=request.POST['description'], posted_by=logged_in)
    new_book.liked_by.add(logged_in)
    return redirect('/books')


def edit_book(request, book_id):
    if 'user_id' not in request.session:
        return redirect('/')
    errors = Book.objects.book_val(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect(f"/books/{book_id}")
    book = Book.objects.get(id=book_id)
    book.title = request.POST['title']
    book.description = request.POST['description']
    book.save()
    return redirect(f"/books/{book_id}")


def delete_book(request, book_id):
    if 'user_id' not in request.session:
        return redirect('/')
    book = Book.objects.get(id=book_id)
    if book.posted_by.id == request.session['user_id']:
        book.delete()
    return redirect("/books")


def fav_book(request, book_id):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    book = Book.objects.get(id=book_id)
    book.liked_by.add(user)
    return redirect(f"/books/{book_id}")


def unfav_book(request, book_id):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    book = Book.objects.get(id=book_id)
    book.liked_by.remove(user)
    return redirect(f"/books/{book_id}")


def one_book(request, book_id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'logged_user': User.objects.get(id=request.session['user_id']),
        'one_book': Book.objects.get(id=book_id)
    }
    return render(request, "onebook.html", context)
