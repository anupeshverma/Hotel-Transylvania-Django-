from django.shortcuts import render


def booking(request, room_type, room_number):
    return render(request, 'booking_form.html', {
        'room_type': room_type,
        'room_number': room_number
    })