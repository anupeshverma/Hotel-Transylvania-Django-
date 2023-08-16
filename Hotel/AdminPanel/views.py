from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from Accounts.models import userAccount
from Booking.models import Booking
from Rooms.models import Room
from django.db.models import Q


# Create your views here.
def getUserAccount(request):
    accn = userAccount.objects.filter(email=request.user.username)
    accn = accn[0]
    return accn


def dashboard(request):
    user_account = getUserAccount(request)
    if user_account.role!="Admin" and user_account.role!="admin":
        return render(request, "error_page.html", {"error": "Unauthorised Access !!"})
    return render(request, "instructions.html", {"acc": user_account})


class addUser(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "add_user.html")


class allBookings(LoginRequiredMixin, View):
    def get(self, request):
        bookings = bookings = Booking.objects.filter().order_by("-id")[:5]
        return render(request, "all_bookings.html", {"bookings": bookings})


class allUsers(LoginRequiredMixin, View):
    def get(self, request):
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
    def post(self, request, userid):
        account = userAccount.objects.get(pk=userid)
        print(account)
        return render(request, 'edit_user.html', {"account":account})


class deleteUser(LoginRequiredMixin, View):
    def post(self, request, userid):
        account = userAccount.objects.get(pk=userid).first()