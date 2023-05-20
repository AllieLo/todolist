from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate


def user_logout(request):
    logout(request)

    return redirect("login")


def user_profile(request):
    return render(request, "user/profile.html")


def user_login(request):
    # print(request.user)
    message = ""
    if request.method == "POST":
        print(request.POST)
        if request.POST.get("register"):
            return redirect("register")

        if request.POST.get("login"):
            username = request.POST.get("username")
            password = request.POST.get("password")

            if password == "" or username == "":
                message = "帳號跟密碼不能為空"
            else:
                # 登入動作
                user = authenticate(request, username=username, password=password)
                print(user)
                if not user:
                    if User.objects.filter(username=username):
                        message = "密碼錯誤"
                    else:
                        message = "帳號錯誤"
                else:
                    login(request, user)
                    message = "登入成功"
                    return redirect("profile")

    return render(request, "user/login.html", {"message": message})


# Create your views here.
def user_register(request):
    message = ""
    form = UserCreationForm()
    if request.method == "GET":
        print("GET")

    if request.method == "POST":
        try:
            # print(User.objects.all())
            username = request.POST.get("username")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            print(username, password1, password2)

            if len(password1) < 8:
                message = "密碼過短"
            elif password1 != password2:
                message = "二次密碼不相符"
            else:
                # 帳號檢查
                if User.objects.filter(username=username).exists():
                    message = "帳號重複"
                else:
                    user = User.objects.create_user(
                        username=username, password=password1
                    ).save()
                    user.save()
                    login(request.user)
                    message = "註冊成功"
                    return redirect("profile")
        except Exception as e:
            print(e)
            message = "註冊失敗"

    return render(request, "user/register.html", {"form": form, "message": message})
