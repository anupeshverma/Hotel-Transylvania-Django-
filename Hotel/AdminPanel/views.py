from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.password_validation import password_validators_help_texts
from Accounts.models import userAccount
from django.db.models import Q
from Booking.models import Booking, currentBookings
from Rooms.models import Room
import os


# Create your views here.
def getUserAccount(request):
    accn = userAccount.objects.filter(email=request.user.username)
    accn = accn[0]
    return accn


def paginator_func(request, queryset, num):
    paginator = Paginator(queryset, int(num))
    page = request.GET.get("page", 1)
    try:
        paginated_data = paginator.get_page(int(page))
    except PageNotAnInteger:
        paginated_data = paginator.get_page(1)
    except EmptyPage:
        paginated_data = paginator.get_page(paginator.num_pages)

    return paginated_data


def dashboard(request):
    user_account = getUserAccount(request)
    if user_account.role != "Admin" and user_account.role != "admin":
        return render(request, "error_page.html", {"error": "Unauthorised Access !!"})
    return render(request, "instructions.html", {"acc": user_account})


class currentBookings_(LoginRequiredMixin, View):
    def get(self, request):
        user_account = getUserAccount(request)
        if user_account.role != "Admin" and user_account.role != "admin":
            return render(
                request, "error_page.html", {"error": "Unauthorised Access !!"}
            )
        bookings = currentBookings.objects.filter().order_by("-bookingDate")
        bookings = paginator_func(request, bookings, 10)

        data = {"bookings": bookings}
        return render(request, "current_bookings.html", data)


class allUsers(LoginRequiredMixin, View):
    def get(self, request):
        user_account = getUserAccount(request)
        if user_account.role != "Admin" and user_account.role != "admin":
            return render(
                request, "error_page.html", {"error": "Unauthorised Access !!"}
            )
        accounts = userAccount.objects.filter().order_by("-first_name")
        admins = userAccount.objects.filter(Q(role="Admin") | Q(role="admin"))
        humans = userAccount.objects.filter(Q(role="Human") | Q(role="human"))
        monsters = userAccount.objects.filter(Q(role="Monster") | Q(role="monster"))

        admins = paginator_func(request, admins, 5)
        # humans= paginator_func(request, humans ,10)
        # monsters = paginator_func(request,monsters,10)
        data = {
            "accounts": accounts,
            "admins": admins,
            "humans": humans,
            "monsters": monsters,
        }
        return render(request, "all_users.html", data)


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
        user = User.objects.create_user(
            username=email, first_name=fname, last_name=lname, password=password
        )
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


class editUser(LoginRequiredMixin, View):
    def get(self, request, userid):
        account = userAccount.objects.get(pk=userid)
        active_status = User.objects.get(username=userid).is_active
        data = {"acc": account, "active": active_status}
        return render(request, "edit_user.html", data)

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
        if request.POST.get("active_status") == "active":
            user_admin.is_active = True
        else:
            user_admin.is_active = False
        user_admin.save()

        url_name = "AdminPanel:all_users"
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

        url_name = "AdminPanel:all_users"
        dynamic_url = reverse(url_name)
        return redirect(dynamic_url)


class allRooms(LoginRequiredMixin, View):
    def get(self, request):
        user_account = getUserAccount(request)
        if user_account.role != "Admin" and user_account.role != "admin":
            return render(
                request, "error_page.html", {"error": "Unauthorised Access !!"}
            )
        rooms = Room.objects.all()
        general = rooms.filter(roomType="General")
        special = rooms.filter(roomType="Special")

        general = paginator_func(request, general, 10)
        special = paginator_func(request, special, 10)

        data = {"general": general, "special": special}
        return render(request, "all_rooms.html", data)


class addRoom(LoginRequiredMixin, View):
    def get(self, request):
        user_account = getUserAccount(request)
        if user_account.role != "Admin" and user_account.role != "admin":
            return render(
                request, "error_page.html", {"error": "Unauthorised Access !!"}
            )
        return render(request, "add_room.html")

    def post(self, request):
        roomNo = request.POST["roomNo"]
        roomType = request.POST["roomType"]
        capacity = request.POST["roomCapacity"]
        price = request.POST["price"]
        roomImage = request.FILES.get("roomImage")
        description = request.POST["description"]

        room = Room(
            roomNo=roomNo,
            roomType=roomType,
            capacity=capacity,
            price=price,
            roomImage=roomImage,
            description=description,
        )
        data = {
            "roomNo": roomNo,
            "roomType": roomType,
            "capacity": capacity,
            "price": price,
            "imageURL": str(roomImage),
            "description": description,
        }

        # Checking if room no.already exist
        if Room.objects.filter(roomNo=roomNo).exists():
            return render(request, "add_room.html", {"error": "Room No. already exist"})
        if roomType == "General" and capacity == "Triple":
            return render(
                request,
                "add_room.html",
                {"error": "General rooms have Single & Double beds only"},
            )
        if roomType == "Special" and capacity == "Single":
            return render(
                request,
                "add_room.html",
                {"error": "Special rooms have Double & Triple beds only"},
            )
        room.save()

        return redirect("Rooms:show_all_rooms")


class editRoom(LoginRequiredMixin, View):
    def get(self, request, roomNo):
        user_account = getUserAccount(request)
        if user_account.role != "Admin" and user_account.role != "admin":
            return render(
                request, "error_page.html", {"error": "Unauthorised Access !!"}
            )
        room = Room.objects.filter(roomNo=roomNo)
        room = room[0]
        return render(request, "edit_room.html", {"room": room})

    def post(self, request, roomNo):
        room = Room.objects.filter(roomNo=roomNo)
        room = room[0]
        roomNo = request.POST["roomNo"]
        roomType = request.POST["roomType"]
        capacity = request.POST["roomCapacity"]
        price = request.POST["price"]
        roomImage = request.FILES.get("roomImage")
        description = request.POST["description"]

        data = {
            "room": room,
            "error": "",
        }

        # Checking if room no.already exist
        if roomType == "General" and capacity == "Triple":
            data["error"] = "General rooms have Single & Double beds only"
            return render(request, "edit_room.html", data)
        if roomType == "Special" and capacity == "Single":
            data["error"] = "Special rooms have Double & Triple beds only"
            return render(request, "edit_room.html", data)

        # Delete previous room image if available
        if roomImage:
            print(roomImage)
            if room.roomImage:
                previous_path = room.roomImage.path
                if os.path.exists(previous_path):
                    os.remove(previous_path)
            room.roomImage = roomImage
        room.roomNo = roomNo
        room.roomType = roomType
        room.capacity = capacity
        room.price = price
        room.description = description
        room.save()

        return redirect("AdminPanel:all_rooms")


class deleteRoom(LoginRequiredMixin, View):
    def get(self, request, roomNo):
        user_account = getUserAccount(request)
        if user_account.role != "Admin" and user_account.role != "admin":
            return render(
                request, "error_page.html", {"error": "Unauthorised Access !!"}
            )
        room = Room.objects.filter(roomNo=roomNo)
        room = room[0]
        room.delete()
        return redirect("AdminPanel:all_rooms")


class allBookings(LoginRequiredMixin, View):
    def get(self, request):
        user_account = getUserAccount(request)
        if user_account.role != "Admin" and user_account.role != "admin":
            return render(
                request, "error_page.html", {"error": "Unauthorised Access !!"}
            )
        bookings = Booking.objects.filter().order_by("checkInDate")
        bookings = paginator_func(request, bookings, 10)
        return render(request, "all_bookings.html", {"bookings": bookings})
