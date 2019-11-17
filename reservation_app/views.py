from django.shortcuts import render, get_object_or_404, redirect
from reservation_app.models import Room, Reservation
from django.http import HttpResponse, request, HttpResponseRedirect
from datetime import date, datetime

# Create your views here.

def add_new_room(request):
    if request.method == "GET":
        dict = {"Response": "Adding new room"}
        return render(request, 'add_new_room.html', dict)
    if request.method == "POST":
        room_name = request.POST.get('room_name')
        room_capacity = int(request.POST.get('room_capacity'))
        if request.POST.get('projector') == "true":
            is_projector = True
        else:
            is_projector = False

        new_room = Room.objects.create(name=f"{room_name}", capacity=room_capacity, is_projector=is_projector)
        new_room.save()
        room_message = f"New room created - {room_name}"

        return render(request, 'add_new_room.html', {"room_message": room_message})


def modify_room(request, id):
    if request.method == "GET":
        room = get_object_or_404(Room, pk=id)
        if room:
            room_dict = {"Room_name": f"Editing {room.name}"}
            return render(request, 'add_new_room.html', room_dict)

    if request.method == "POST":
        new_room_name = request.POST.get('room_name')
        new_room_capacity = int(request.POST.get('room_capacity'))
        if request.POST.get('projector') == "true":
            new_is_projector = True
        else:
            new_is_projector = False

        room = Room.objects.get(pk=id)
        old_room_name = room.name
        old_room_capacity = room.capacity
        old_is_projector = room.is_projector

        room_message = f"Modified! \n " \
                       f"Old room name: {old_room_name} / New room {new_room_name} \n" \
                       f" Old max. capacity {old_room_capacity} / New max. capacity {new_room_capacity}.\n" \
                       f" Old projector status: {old_is_projector} / New projector status: {new_is_projector}"

        room.name = new_room_name
        room.capacity = new_room_capacity
        room.is_projector = new_is_projector
        room.save()

        return render(request, 'add_new_room.html', {"room_message": room_message})


def delete_room(request, id):
    room = Room.objects.get(id=id)
    response = f"Deleted room {room.name} - ID {room.id}"
    room.delete()
    # return HttpResponse(response)
    return render(request, 'info.html', {"response": response, "response2": "Deletion successful!"})
def get_room_details(request, id):
    room = Room.objects.get(id=id)
    today = date.today()
    reservations = Reservation.objects.filter(room_id=id).filter(date__gte=today)
    response = ""
    for reservation in reservations:
        response += f"{reservation.date}, "

    room_dict = {"Room_name": room.name,
                 "Room_capacity": room.capacity,
                 "Is_projector": room.is_projector,
                 "Room_id": room.id,
                 "Reservations": response}

    return render(request, 'room_details.html', room_dict)

def get_all_rooms(request):
    all_rooms = Room.objects.all()
    all_rooms = {"all_rooms": all_rooms}
    return render(request, 'all_rooms.html', all_rooms)

def search_rooms(request):
    if request.GET.get('room_name') != "" and request.GET.get('room_capacity') == "" and request.GET.get('projector') == "" and request.GET.get('reservation_date') == "":
        room_name = request.GET.get('room_name')
        room = Room.objects.get(name=room_name)
        return HttpResponseRedirect(f'/room/{room.id}')

    if request.GET.get('room_name') != "" and request.GET.get('room_capacity') != "":
        room_name = request.GET.get('room_name')
        room_capacity = int(request.GET.get('room_capacity'))
        if request.GET.get('projector') == "true":
            is_projector = True
        else:
            is_projector = False
        room = Room.objects.get(name=f"{room_name}", capacity=room_capacity, is_projector=is_projector)
        room_id = room.id
        return HttpResponseRedirect(f'/room/{room_id}')

    if request.GET.get('room_name') == "" and request.GET.get('room_capacity') != "" \
            and request.GET.get('reservation_date') != "":
        reservation_date = request.GET.get('reservation_date')
        room_capacity = int(request.GET.get('room_capacity'))
        rooms = Room.objects.filter(capacity__gte=room_capacity)
        res_list = Reservation.objects.filter(room_id__id__in=[room.id for room in rooms], date=reservation_date)
        response = ""

        if len(res_list) > 0:
            asd = []
            for res in res_list:
                for room in rooms:
                    if res.room_id.id != room.id:
                        asd.append(room)
            for room in asd:
                response += f"Free room: {room.name}"
            return HttpResponse(f"{response}")
        else:
            for room in rooms:
                response += f"Free room: {room.name}"
            return HttpResponse(response)

        # date_time_obj = datetime.strptime(reservation_date, '%Y-%m-%d')
        # today = datetime.today()
        #
        # room_capacity = int(request.GET.get('room_capacity'))
        # rooms = Room.objects.filter(capacity__gte=room_capacity)
        #
        # return render(request, 'search_result.html', {"rooms": rooms})

    return HttpResponse ("test")

def create_reservation(request, id):
    reservation_date = request.POST.get('reservation')
    date_time_obj = datetime.strptime(reservation_date, '%Y-%m-%d')
    today = datetime.today()
    if today < date_time_obj:
        room = Room.objects.get(id=id)
        date_list = Reservation.objects.filter(date=reservation_date, room_id=room)
        if len(date_list) == 1:
            return HttpResponse("Reservation already exists")
        else:
            reservation = Reservation.objects.create(date=reservation_date, room_id=room)
            reservation.save()
            return HttpResponse("Reservation created")
    return HttpResponse("Can't create past reservations!")


