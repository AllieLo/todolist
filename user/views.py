from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
                    User.objects.create_user(
                        username=username, password=password1
                    ).save()
                    message = "註冊成功"
        except Exception as e:
            print(e)
            message = "註冊失敗"

    return render(request, "user/register.html", {"form": form, "message": message})
