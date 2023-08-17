from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseServerError
import string
from django.views import View
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, BadHeaderError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.contrib import admin
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.password_validation import password_validators_help_texts
from .models import *
from Booking.models import Booking
import random
import os
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def checkrender(request):
    return render(request, "change_password.html")


# Create your views here.
def userlogin(request):
    if request.method == "GET":
        return render(request, "login.html")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user_account = userAccount.objects.filter(email=email)
        if user_account:
            # If user is in admin user and is active
            if User.objects.filter(username=email).first().is_active:
                user = authenticate(username=email, password=password)
                if user is not None:
                    login(request, user)
                    next_url = request.GET.get('next')
                    print(next_url)
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect('home')
                else:
                    return render(
                        request, "login.html", {"error": "Invalid Email or Password"}
                    )
            # If the user is in database but not active
            else:
                return render(
                    request,
                    "activation_email.html",
                    {"error": "Your account is not Active. Activate First"},
                )
        else:
            return render(
                request, "login.html", {"error": "No user exist with this Email."}
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
        mail_subject = "Activation link has been sent to your email."
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
            {"error": "Please confirm your email address to activate youe account."},
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
        return render(
            request,
            "error_page.html",
            {
                "error": "Thank You For Your Email Confirmation.\n\nNow LogIn to your account."
            },
        )
    else:
        return render(
            request, "error_page.html", {"error": "Activation Link Is Invalid."}
        )


def resendActivationEmail(request):
    if request.method == "GET":
        return render(request, "resend_activation_email.html")

    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            return render(
                request,
                "error_page.html",
                {"error": "No account exists with this email. Sign up first."},
            )
        # If user is found and not active
        if user.is_active == False:
            current_site = get_current_site(request)
            mail_subject = "Activation link has been sent to your Email."
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
            return render(
                request,
                "error_page.html",
                {
                    "error": "Please confirm your email address to activate the account"
                },
            )
        # User exist and account is already activatedd.
        else:
            return render(
                request,
                "error_page.html",
                {"error": "Account is already activated. Try LogIn."},
            )


class profile(LoginRequiredMixin, View):
    def get(self, request):
        user_account = userAccount.objects.filter(email=request.user.username)
        print(user_account)
        if not user_account:
            logout(request)
            return render(request, "error_page.html", {"error": "No Profile Found"})
        
        user_account = user_account[0]
        bookings = Booking.objects.filter(user=user_account).order_by('-bookingDate')

        paginator = Paginator(bookings, 2)  # Show 2 bookings  per page
        page = request.GET.get('page', 1)
        try:
            bookings = paginator.get_page(page)
        except PageNotAnInteger:
            bookings = paginator.get_page(1)
        except EmptyPage:
            bookings = paginator.get_page(paginator.num_pages)


        return render(request, "profile_page.html", {"acc": user_account, "bookings": bookings})


def editProfile(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return render(request, "login.html", {"error": "LogIn to account first !"})
        user_account = userAccount.objects.filter(email=request.user.username)
        if not user_account:
            logout(request)
            return render(
                request, "error_page.html", {"error": "No Profile Found. Try LogIn"}
            )

        user_account = user_account[0]
        return render(request, "edit_profile.html", {"acc": user_account})

    if request.method == "POST":
        user_account = userAccount.objects.filter(email=request.user.username)
        user_account = user_account[0]
        # Edit details in the database table
        user_account.first_name = request.POST.get("fname")
        user_account.last_name = request.POST.get("lname")
        user_account.email = request.POST.get("email")
        user_account.phone_number = request.POST.get("contact")
        user_account.role = request.POST.get("role")
        user_account.save()
        # Edit details in the admin user
        user_admin = User.objects.get(username=request.user.username)
        user_admin.first_name = request.POST.get("fname")
        user_admin.last_name = request.POST.get("lname")
        user_admin.username = request.POST.get("email")
        user_admin.save()
        return redirect("Accounts:profile")


def deleteProfile(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return render(request, "login.html", {"error": "LogIn to account first !"})
        # generate an otp and send it to user email
        otp = random.randint(100000, 999999)
        request.session["otp"] = otp
        user_account = userAccount.objects.filter(email=request.user.username)
        user_account = user_account[0]
        # sent the mail to the user
        message = f"Hi {user_account.first_name}c,\n\nYour OTP for acount deletion is {otp}. Do not share it with anyone."
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
        user_otp = request.POST.get("otp")
        stored_otp = request.session.get("otp")
        user_account = userAccount.objects.filter(email=request.user.username)
        user_account = user_account[0]

        if user_account and str(user_otp) == str(stored_otp):
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
            del request.session["otp"]
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


def changePassword(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return render(request, "login.html", {"error": "LogIn to account first !"})
        return render(request, "change_password.html")

    if request.method == "POST":
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

        user_email = request.session.get("email")
        user = User.objects.get(username=user_email)
        print(user)
        user.set_password(new_password)
        user.save()
        del request.session["email"]
        user = authenticate(username=user_email, password=new_password)
        login(request, user)
        return redirect("Accounts:profile")


def forgotPassword(request):
    if request.method == "GET":
        return render(request, "forgot_password.html")
    
    if request.method == "POST":
        email = request.POST.get("email")
        request.session["email"] = email
        print(email)
        user_account = userAccount.objects.filter(email=email)
        # check if there is a user in database with this email
        if not user_account:
            return render(
                request,
                "error_page.html",
                {"error": "There is no account with this email."},
            )
        else:
            # Check if the user is activated or not
            if not User.objects.filter(username=email).first().is_active:
                return render(
                    request, "error_page.html", {"error": "Your account is not active."}
                )
            else:
                user_account = user_account[0]
                otp = random.randrange(100000, 999999)
                request.session["otp"] = otp

                # Send email
                message = f"Hi {user_account.first_name},\n\nYour OTP for reset password is {otp}. Do not share it with anyone."
                mail_subject = "Reset Password OTP"
                email = EmailMessage(mail_subject, message, to=[user_account.email])
                try:
                    email.send()
                    return render(request, "otp_verification.html")
                except BadHeaderError:
                    return HttpResponseServerError(
                        "An error occurred while sending the email. Please try again later."
                    )


def otpVerification(request):
    if request.method == "GET":
        otp = random.randint(100000, 999999)
        request.session["otp"] = otp
        if request.user.is_authenticated:
            request.session["email"] = request.user.username
        elif request.GET.get("email"):
            print(request.GET.get("email"))
            request.session["email"] = request.GET.get("email")
        else:
            render(request, "error_page.html", {"error": "Unknown Error Occurred."})

        user_email = request.session.get("email")
        print(user_email)
        user_account = userAccount.objects.filter(email=user_email)
        user_account = user_account[0]

        # sent the mail to the user
        message = f"Hi {user_account.first_name},\n\nYour OTP for password change is {otp}. Do not share it with anyone."
        mail_subject = "Password Change Confirmation OTP"
        email = EmailMessage(mail_subject, message, to=[user_account.email])
        try:
            email.send()
            return render(request, "otp_verification.html")
        except BadHeaderError:
            return HttpResponseServerError(
                "An error occurred while sending the email. Please try again later."
            )
    if request.method == "POST":
        user_otp = request.POST.get("otp")
        stored_otp = request.session.get("otp")
        if str(user_otp) == str(stored_otp):
            del request.session["otp"]
            return render(request, "change_password.html")
        else:
            return render(request, "otp_verification.html", {"error": "OTP Incorrect"})
