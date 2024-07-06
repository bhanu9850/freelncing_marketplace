from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Message
from .forms import MessageForm
from freelancer.views import *
from client.views import *
@login_required
@login_required
def inbox(request):
    received_messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    
    return render(request, 'inbox.html', {
        'received_messages': received_messages,
        'sent_messages': sent_messages,
    })

@login_required
def send_message(request, receiver_username=None):
    if receiver_username:
        receiver = get_object_or_404(User, username=receiver_username)
        print(f'Debug: Receiver found: {receiver.username}')
    else:
        receiver = None
        print('Debug: No receiver username provided.')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            if not receiver:
                print('Debug: Receiver not found when trying to send the message.')
                return redirect('some_error_page')  # Handle this appropriately
            message.receiver = receiver
            message.save()
            print(f'Debug: Message sent from {request.user.username} to {receiver.username}')
            return redirect('inbox')
        else:
            print('Debug: Form is not valid.')
    else:
        form = MessageForm()

    print(f'Debug: Sending message form rendered for sender {request.user.username} and receiver {receiver.username if receiver else "None"}')
    return render(request, 'send_message.html', {'form': form, 'receiver': receiver})