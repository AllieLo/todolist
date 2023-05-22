from django.shortcuts import render, redirect
from .models import Todo
from .forms import TodoForm
from datetime import datetime


def create_todo(request):
    message = ""
    form = TodoForm()
    if request.method == "POST":
        form = TodoForm(request.POST)
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()
        message = "建立Todo成功"
        return redirect("todolist")
    return render(request, "todo/create_todo.html", {"form": form, "message": message})


def todo(request, id):
    todo = None
    message = ""
    try:
        if request.method == "GET":
            # 將取得的todo事項給表單
            todo = Todo.objects.get(pk=id)
            form = TodoForm(instance=todo)
        if request.method == "POST":
            print(request.POST)
            form = TodoForm(request.POST, instance=todo)
            if form.is_valid():
                todo = form.save(commit=False)
                if todo.completed:
                    todo.date_completed = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                todo.save()
                message = "更新成功"
    except Exception as e:
        print(e)
        message = "更新失敗"
    return render(
        request, "todo/todo.html", {"todo": todo, "form": form, "message": message}
    )


def todolist(request):
    todos = None
    user = request.user
    if user.is_authenticated:
        todos = Todo.objects.filter(user=user)

    return render(request, "todo/todolist.html", {"todos": todos})
