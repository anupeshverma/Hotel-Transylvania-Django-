from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseServerError
import string
from django.views import View
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, BadHeaderError
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.contrib import admin
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.password_validation import (
    validate_password,
    password_validators_help_texts,
)


from .models import *
import random
import os


# Create your views here.
def userlogin(request):
    if request.method == "GET":
        return render(request, "login.html")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user_account = userAccount.objects.filter(email=email)
        if user_account:
            print(user_account)
            if User.objects.filter(username=email).first().is_active:
                user = authenticate(username=email, password=password)
                print(user)
                if user is not None:
                    login(request, user)
                    return redirect("home")
                else:
                    return render(
                        request, "login.html", {"error": "Invalid E-mail or Password"}
                    )
            else:
                return render(
                    request,
                    "error_page.html",
                    {"error": "Your account is not Active. Activate First"},
                )
        else:
            return render(
                request, "login.html", {"error": "Invalid E-mail or Password"}
            )


def userlogout(request):
    logout(request)
    return redirect("/")


def userSignup(request):
    if request.method == "GET":
        return render(request, "signup.html")

    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        contact = request.POST["contact"]
        role = request.POST["role"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        data = {
            "fname": fname,
            "lname": lname,
            "email": email,
            "contact": contact,
            "role": role,
            "error": 0,
        }

        # Checking if email is already in use
        if (
            User.objects.filter(username=email).exists()
            and userAccount.objects.filter(email=email).exists()
        ):
            data["error"] = 1
            return render(request, "signup.html", data)

        if password != confirm_password:
            data["error"] = 2
            return render(request, "signup.html", data)

        try:
            validate_password(password)
        except ValidationError as e:
            data["error"] = 3
            return render(request, "signup.html", data)

        if checkPhone(contact):
            data["error"] = 4
            return render(request, "signup.html", data)

        user = User.objects.create_user(
            username=email, first_name=fname, last_name=lname, password=password
        )
        user.set_password(password)
        user.is_active = False

        current_site = get_current_site(request)
        mail_subject = "Activation link has been sent to your email id"
        message = render_to_string(
            "email_activation.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            },
        )
        to_email = email
        email = EmailMessage(mail_subject, message, to=[to_email])
        try:
            email.send()

        except BadHeaderError:
            return HttpResponseServerError(
                "An error occurred while sending the email. Please try again later."
            )
        try:
            user.full_clean()
            user.save()
            new_user = userAccount(
                first_name=fname,
                last_name=lname,
                role=role,
                email=to_email,
                phone_number=contact,
            )
            new_user.save()
        except ValidationError as e:
            data["error"] = "Something Went Wrong !"
            return render(request, "signup.html", data)
        return render(
            request,
            "error_page.html",
            {"error": "Please confirm your email address to complete the registration"},
        )


def checkPhone(contact):
    for ch in contact:
        if not ch in string.digits:
            return True
    return False


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        logout(request)
        return render(request, 'error_page.html', {"error":"Thank You For Your Email Confirmation."})
    else:
        return render(request, 'error_page.html', {"error":"Activation Link Is Invalid."})


class profile(LoginRequiredMixin, View):
    def get(self, request):
        user_account = userAccount.objects.filter(email=request.user.username)
        print(user_account)
        if not user_account:
            logout(request)
            return render(request, 'error_page.html', {"error":"No Profile Found"})

        user_account = user_account[0]
        return render(request, "profile_page.html", {"acc": user_account})


def editProfile(request):
    if request.method == "GET":
        user_account = userAccount.objects.filter(email=request.user.username)
        if not user_account:
            return HttpResponse("No profile found")

        user_account = user_account[0]
        return render(request, "edit_profile.html", {"acc": user_account})

    if request.method == "POST":
        user_account = userAccount.objects.filter(email=request.user.username)
        user_account = user_account[0]
        user_account.first_name = request.POST.get("fname")
        user_account.last_name = request.POST.get("lname")
        user_account.email = request.POST.get("email")
        user_account.phone_number = request.POST.get("contact")
        user_account.role = request.POST.get("role")
        user_account.save()
        return redirect("Accounts:profile")


otp_storage = 0


def deleteProfile(request):
    if request.method == "GET":
        # generate an otp and send it to user email
        otp = random.randint(100000, 999999)
        global otp_storage
        otp_storage = otp
        user_account = userAccount.objects.filter(email=request.user.username)
        user_account = user_account[0]
        # sent the mail to the user
        data = {
            "otp": otp,
            "user_account": user_account,
        }
        message = render_to_string("email_deletion.html", data)
        mail_subject = "Account Deletion Confirmation OTP"
        email = EmailMessage(mail_subject, message, to=[user_account.email])
        try:
            email.send()
            return render(request, "confirm_delete.html")
        except BadHeaderError:
            return HttpResponseServerError(
                "An error occurred while sending the email. Please try again later."
            )

    if request.method == "POST":
        otp = request.POST.get("otp")
        user_account = userAccount.objects.filter(email=request.user.username)
        user_account = user_account[0]

        if user_account and str(otp) == str(otp_storage):
            # Delete the profile photo if it exists
            if user_account.profile_pic:
                previous_photo_path = user_account.profile_pic.path
                if os.path.exists(previous_photo_path):
                    os.remove(previous_photo_path)

            # Delete the user from the django admin also
            user = User.objects.get(username=user_account.email)
            user.delete()

            # Delete the user from the database
            user_account.delete()
            userlogout(request)
            return redirect("home")
    return render(request, "confirm_delete.html", {"error": "Enter correct OTP !"})


def editPhoto(request):
    if request.method == "POST":
        profile_photo = request.FILES.get("profile_photo")
        user_account = userAccount.objects.get(email=request.user.username)

        # Delete the previous profile photo if it exists
        if user_account.profile_pic:
            previous_photo_path = user_account.profile_pic.path
            if os.path.exists(previous_photo_path):
                os.remove(previous_photo_path)

        # Save the uploaded file as the new profile photo
        user_account.profile_pic = profile_photo
        user_account.save()
        return redirect("Accounts:profile")
    return render(request, "profile_page.html", {"acc": user_account})


class change_password(LoginRequiredMixin, View):
    def get(self, request):
        otp = random.randint(100000, 999999)
        request.session["otp"] = otp
        user_account = userAccount.objects.filter(email=request.user.username)
        user_account = user_account[0]

        # sent the mail to the user
        message = f"Hi {user_account.first_name},\n\nYour OTP for password change is {otp}. Do not share it with anyone."
        mail_subject = "Passworcd Change Confirmation OTP"
        email = EmailMessage(mail_subject, message, to=[user_account.email])
        try:
            email.send()
            return render(request, "change_password.html")
        except BadHeaderError:
            return HttpResponseServerError(
                "An error occurred while sending the email. Please try again later."
            )

    def post(self, request):
        user_otp = request.POST.get("otp")
        stored_otp = request.session.get("otp")
        if str(user_otp) == str(stored_otp):
            # if the otp is correct
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")
            # if the passwords are the same
            if new_password != confirm_password:
                return render(
                    request, "change_password.html", {"error": "Password Do Not Match"}
                )
            try:
                validate_password(new_password)
            except ValidationError as e:
                error_message = "\n".join(e.messages)
                error_message += "\n\n" + password_validators_help_texts()
                # Optional: Include password requirements
                return render(request, "change_password.html", {"error": error_message})

            user = get_user_model().objects.get(username=request.user.username)
            print(user)
            user.set_password(new_password)
            user.save()
            del request.session["otp"]
            user = authenticate(username=request.user.username, password=new_password)
            login(request, user)
            return redirect("Accounts:profile")

        else:
            return render(request, "change_password.html", {"error": "OTP Incorrect"})
