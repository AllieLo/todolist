from django.shortcuts import render, redirect
from .models import Todo
from .forms import TodoForm
from datetime import datetime
from django.contrib.auth.decorators import login_required


@login_required
def completed_todo(request):
    todos = None
    user = request.user
    if user.is_authenticated:
        todos = Todo.objects.filter(user=user).order_by("-date_completed")

    return render(request, "todo/completed_todo.html", {"todos": todos})


@login_required
def create_todo(request):
    message = ""
    form = TodoForm()
    try:
        if request.method == "POST":
            form = TodoForm(request.POST)
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            message = "建立Todo成功"
            return redirect("todolist")
    except Exception as e:
        print(e)
        message = "建立Todo失敗"
    return render(request, "todo/create_todo.html", {"form": form, "message": message})


@login_required
def todo(request, id):
    todo, form = None, None
    message = ""
    try:
        todo = Todo.objects.get(pk=id)
        # 只能檢視自己的待辦事項
        if todo.user.id != request.user.id:
            todo = None

        elif request.method == "GET":
            # 將取得的todo事項給表單
            # todo = Todo.objects.get(pk=id)
            form = TodoForm(instance=todo)
        elif request.method == "POST":
            if request.POST.get("update"):
                form = TodoForm(request.POST, instance=todo)
                if form.is_valid():
                    todo = form.save(commit=False)
                    if todo.completed:
                        todo.date_completed = datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                    todo.user = request.user
                    todo.save()
                    message = "更新成功"
            if request.POST.get("delete"):
                todo.delete()
                return redirect("todolist")

    except Exception as e:
        print(e)
        message = "更新失敗"
    return render(
        request, "todo/todo.html", {"todo": todo, "form": form, "message": message}
    )


@login_required
def todolist(request):
    todos = None
    user = request.user
    if user.is_authenticated:
        todos = Todo.objects.filter(user=user).order_by("-created")

    return render(request, "todo/todolist.html", {"todos": todos})
