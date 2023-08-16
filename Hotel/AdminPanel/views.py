from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.password_validation import password_validators_help_texts
from Accounts.models import userAccount
from django.db.models import Q
from Booking.models import Booking
from Rooms.models import Room


# Create your views here.
def getUserAccount(request):
    accn = userAccount.objects.filter(email=request.user.username)
    accn = accn[0]
    return accn


def dashboard(request):
    user_account = getUserAccount(request)
    if user_account.role != "Admin" and user_account.role != "admin":
        return render(request, "error_page.html", {"error": "Unauthorised Access !!"})
    return render(request, "instructions.html", {"acc": user_account})


class addUser(LoginRequiredMixin, View):
    def get(self, request):
        user_account = getUserAccount(request)
        if user_account.role != "Admin" and user_account.role != "admin":
            return render(
                request, "error_page.html", {"error": "Unauthorised Access !!"}
            )

        return render(request, "add_user.html")

    def post(self, request):
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        contact = request.POST["contact"]
        role = request.POST["role"]
        password = request.POST["password"]


        data = {
            "fname": fname,
            "lname": lname,
            "email": email,
            "contact": contact,
            "role": role,
        }

        # Checking if email is already in use
        if (
            User.objects.filter(username=email).exists()
            and userAccount.objects.filter(email=email).exists()
        ):
            return render(request, "add_user.html", {"error": "Email already exist !!"})
        try:
            validate_password(password)
        except ValidationError as e:
            return render(request, "add_user.html", {"error": "Enter Secure Password"})
        user = User.objects.create_user(username=email, first_name=fname, last_name=lname, password=password)
        user.save()
        new_user = userAccount(
            first_name=fname,
            last_name=lname,
            role=role,
            email=email,
            phone_number=contact,
        )
        new_user.save()
        return render(request, "instructions.html")


class allUsers(LoginRequiredMixin, View):
    def get(self, request):
        user_account = getUserAccount(request)
        if user_account.role != "Admin" and user_account.role != "admin":
            return render(
                request, "error_page.html", {"error": "Unauthorised Access !!"}
            )
        accounts = userAccount.objects.filter().order_by("-first_name")
        admins = userAccount.objects.filter(Q(role="Admin") | Q(role="admin"))
        print(admins)
        humans = userAccount.objects.filter(Q(role="Human") | Q(role="human"))
        monsters = userAccount.objects.filter(Q(role="Monster") | Q(role="monster"))
        data = {
            "accounts": accounts,
            "admins": admins,
            "humans": humans,
            "monsters": monsters,
        }
        return render(request, "all_users.html", data)


class editUser(LoginRequiredMixin, View):
    def get(self, request, userid):
        account = userAccount.objects.get(pk=userid)
        return render(request, "edit_user.html", {"acc": account})
    def post(self, request, userid):
        user_account = userAccount.objects.filter(email=request.POST.get("email"))
        user_account = user_account[0]
        # Edit details in the database table
        user_account.first_name = request.POST.get("fname")
        user_account.last_name = request.POST.get("lname")
        user_account.email = request.POST.get("email")
        user_account.phone_number = request.POST.get("contact")
        user_account.role = request.POST.get("role")
        user_account.save()
        # Edit details in the admin user
        user_admin = User.objects.get(username=request.POST.get("email"))
        user_admin.first_name = request.POST.get("fname")
        user_admin.last_name = request.POST.get("lname")
        user_admin.username = request.POST.get("email")
        user_admin.save()

        url_name = 'AdminPanel:all_users'
        dynamic_url = reverse(url_name)
        return redirect(dynamic_url)


class deleteUser(LoginRequiredMixin, View):
    def get(self, request, userid):
        user_account = getUserAccount(request)
        if user_account.role != "Admin" and user_account.role != "admin":
            return render(
                request, "error_page.html", {"error": "Unauthorised Access !!"}
            )
        account = userAccount.objects.get(pk=userid)
        mUser = User.objects.filter(username=userid)
        mUser.delete()
        account.delete()

        url_name = 'AdminPanel:all_users'
        dynamic_url = reverse(url_name)
        return redirect(dynamic_url)
    

class allBookings(LoginRequiredMixin, View):
    def get(self, request):
        user_account = getUserAccount(request)
        if user_account.role != "Admin" and user_account.role != "admin":
            return render(
                request, "error_page.html", {"error": "Unauthorised Access !!"}
            )
        bookings = bookings = Booking.objects.filter().order_by("-id")[:5]
        return render(request, "all_bookings.html", {"bookings": bookings})
