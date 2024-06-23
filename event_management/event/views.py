from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from event.models import User, Event, Registration
from event.forms import CreateUserForm, CreateEventForm
from .serializers import UserSerializer, EventSerializer
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .decorators import login_required_view, organizer_required, admin_required

# View for user registration
class Register(APIView):
    def get(self, request):
        form = CreateUserForm()
        context = {'form': form}
        return render(request, "register.html", context)
    
    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
        else:
            context = {'form': form}
            return render(request, "register.html", context)

# View for listing events for an organizer
@method_decorator(organizer_required, name='dispatch')
class EventList(APIView):
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')
        events = Event.objects.filter(organizer_id=user_id)
        serializer = EventSerializer(events, many=True)
        context = {'data': serializer.data}
        return render(request, 'viewevent.html', context)

# View for creating events
@method_decorator(organizer_required, name='dispatch')
class CreateEvent(APIView):
    def get(self, request):
        form = CreateEventForm()
        context = {'form': form}
        return render(request, 'addevent.html', context)
    
    def post(self, request):
        form = CreateEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = User.objects.get(id=request.session['user_id'])
            event.save()
            messages.success(request,'Event Created')
            return redirect('event_list')
        context = {'form': form}
        return render(request, 'addevent.html', context)

# View for user login
class Login(APIView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['user_id'] = user.pk
            if user.role == 'organizer':
                return HttpResponse("<script>alert('Login Successfull');window.location='events'</script>")
            elif user.role == 'admin':
                return HttpResponse("<script>alert('Login Successfull');window.location='adminhome'</script>")
            else:
                return HttpResponse("<script>alert('Login Successfull');window.location='home'</script>")
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

# View for logout
class Logout(APIView):
    def get(self, request):
        logout(request)
        return redirect('login')

    def post(self, request):
        logout(request)
        return redirect('login')

# View for home page displaying all events
class Home(APIView):
    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        context = {'data': serializer.data}
        return render(request, 'home.html', context)

# View for deleting an event
@method_decorator(organizer_required, name='dispatch')
class Delete(APIView):
    def get(self, request, id):
        event = get_object_or_404(Event, id=id)
        event.delete()
        return redirect('event_list')

# View for updating an event
@method_decorator(organizer_required, name='dispatch')
class Update(APIView):
    def get(self, request, id):
        event = get_object_or_404(Event, id=id)
        form = CreateEventForm(instance=event)
        context = {'form': form}
        return render(request, 'updateevent.html', context)

    def post(self, request, id):
        event = get_object_or_404(Event, id=id)
        form = CreateEventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request,'Event Updated')
            return redirect('event_list')
        context = {'form': form}
        return render(request, 'addevent.html', context)

# View for registering a user to an event
@method_decorator(login_required_view, name='dispatch')
class RegisterEvent(APIView):
    def get(self, request, id):
        user_id = request.session.get('user_id')
        if not user_id:
            messages.error(request, 'User not logged in.')
            return redirect('home')
        if Registration.objects.filter(event_id=id, attendee_id=user_id).exists():
            messages.success(request, 'Already registered')
        else:
            Registration.objects.create(event_id=id, attendee_id=user_id)
            messages.success(request, 'Successfully registered')
        return redirect('home')

# View for Admin Home page
@method_decorator(admin_required, name='dispatch')
class AdminHome(APIView):
    def get(self, request):
        event = Event.objects.all()
        total_users = User.objects.count()
        total_events = Event.objects.count()
        total_registrations = Registration.objects.count()
        data = {
            'total_users': total_users,
            'total_events': total_events,
            'total_registrations': total_registrations,
        }
        context = {'data': data, 'event': event}
        return render(request, 'adminhome.html', context)
