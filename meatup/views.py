from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
from .models import Message
from .forms import MessageEntryForm
from main.models import UserProfile
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
@login_required(login_url='/login')
def meatup_home(request):
    user = request.user
    sender_user_profile = UserProfile.objects.get(user=user)
    sent_messages = Message.objects.filter(sender=sender_user_profile).order_by('-timestamp')
    receiver_user_profile = UserProfile.objects.get(user=user)
    received_messages = Message.objects.filter(receiver=receiver_user_profile).order_by('-timestamp')

    context = {
        'sent_messages': sent_messages,
        'received_messages': received_messages,
    }
    return render(request, 'meatup.html', context)

@csrf_exempt
@login_required(login_url='/login')
def create_message_entry(request):
    if request.method == "POST":
        form = MessageEntryForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            user_profile = UserProfile.objects.get(user=request.user)
            new_message.sender = user_profile
            new_message.save()
            return redirect(reverse('meatup:meatup_home'))
    else:
        form = MessageEntryForm()

    # Pass the form to the template
    context = {'form': form}
    return render(request, 'create_message_entry.html', context)

@csrf_exempt
@login_required(login_url='/login')
def delete_message(request, id):
    user_profile = UserProfile.objects.get(user=request.user)
    message = get_object_or_404(Message, id=id)
    message.delete()
    return redirect('meatup:meatup_home')

@csrf_exempt
@login_required(login_url='/login')
def edit_message(request, id):
    # Edit pesan tertentu
    message = get_object_or_404(Message, id=id)
    if request.method == "POST":
        form = MessageEntryForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('meatup:meatup_home'))
    else:
        form = MessageEntryForm(instance=message)

    context = {'form': form, 'message_id': id}
    return render(request, 'create_message_entry.html', context)

@csrf_exempt
@login_required(login_url='/login')
def meatup_home_flutter(request):
    user = request.user
    sender_user_profile = UserProfile.objects.get(user=user)
    sent_messages = Message.objects.filter(sender=sender_user_profile).order_by('-timestamp').values()
    receiver_user_profile = UserProfile.objects.get(user=user)
    received_messages = Message.objects.filter(receiver=receiver_user_profile).order_by('-timestamp').values()

    response_data = {
        'sent_messages': list(sent_messages),
        'received_messages': list(received_messages),
    }
    return JsonResponse(response_data, safe=False)

@csrf_exempt
@login_required(login_url='/login')
def create_message_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        sender_user_profile = UserProfile.objects.get(user=request.user)

        receiver_user_profile = get_object_or_404(UserProfile, id=data.get("receiver_id"))
        new_message = Message.objects.create(
            sender=sender_user_profile,
            receiver=receiver_user_profile,
            title=data.get("title"),
            content=data.get("content"),
        )
        new_message.save()

        return JsonResponse({"status": "success", "message": "Message created successfully."}, status=201)
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)

@csrf_exempt
@login_required(login_url='/login')
def delete_message_flutter(request, id):
    user_profile = UserProfile.objects.get(user=request.user)
    message = get_object_or_404(Message, id=id)

    if message.sender == user_profile:
        message.delete()
        return JsonResponse({"status": "success", "message": "Message deleted successfully."}, status=200)

    return JsonResponse({"status": "error", "message": "Unauthorized action."}, status=403)

@csrf_exempt
@login_required(login_url='/login')
def edit_message_flutter(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = get_object_or_404(Message, id=id)

        if message.sender.user == request.user:
            message.title = data.get("title", message.title)
            message.content = data.get("content", message.content)
            message.save()

            return JsonResponse({"status": "success", "message": "Message updated successfully."}, status=200)

        return JsonResponse({"status": "error", "message": "Unauthorized action."}, status=403)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)