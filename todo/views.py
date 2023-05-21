from django.shortcuts import render
from .models import Todo


# Create your views here.
def todo(request):
    todos = Todo.objects.all()
    return render(request, "todo/todo.html", {"todos": todos})
