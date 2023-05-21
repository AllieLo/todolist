from django.shortcuts import render
from .models import Todo
from .forms import TodoForm


# Create your views here.
def create_todo(request):
    message = ""
    form = TodoForm()
    if request.method == "POST":
        form = TodoForm(request.POST)
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()
        message = "建立Todo成功"
    return render(request, "todo/create_todo.html", {"form": form, "message": message})


def todo(request, id):
    todo = None
    try:
        todo = Todo.objects.get(pk=id)
    except Exception as e:
        print(e)
    return render(request, "todo/todo.html", {"todo": todo})


def todolist(request):
    todos = None
    user = request.user
    if user.is_authenticated:
        todos = Todo.objects.filter(user=user)

    return render(request, "todo/todolist.html", {"todos": todos})
