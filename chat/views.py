from django.shortcuts import render, get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from .models import ChatGroup, GroupMessage
from .forms import ChatMessageCreateForm
from django.contrib.auth.models import User
from django.http import Http404
import shortuuid

@login_required
def chat_view(request, chatroom_name="Public-chat"):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    chat_messages = chat_group.chat_messages.all()[:30]

    # Determine the other user in private chats
    other_user = None
    if chat_group.is_private:
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break
                
    # HTMX POST: save new message
    if request.method == 'POST' and request.htmx:
        form = ChatMessageCreateForm(request.POST)
              
        # print("POST data:", request.POST)  
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            print("Message saved:", message.body)
            context = {'message': message, 'user': request.user}
            
            return render(request, 'chat/partials/chat_message_p.html', context)
        else:
            print("Form invalid:", form.errors)

    # Regular GET
    form = ChatMessageCreateForm()
    
    context = {
        'chat_messages': chat_messages,
        'form': form,
        # 'chat_group': chat_group,
        # 'user': request.user,
        'other_user': other_user,
        'chatroom_name': chatroom_name,
    }
    
    return render(request, 'chat/chat.html', context)

# get_or_create_chatroom view
@login_required
def get_or_create_chatroom_view(request, username):
    if request.user.username == username:
        return redirect('chat') # Prevent chatting with oneself
    
    other_user = User.objects.get(username=username)
    my_private_chatrooms = request.user.chat_groups.filter(is_private=True)

    if my_private_chatrooms.exists():
        for chatroom in my_private_chatrooms:
            if other_user in chatroom.members.all():
                return redirect('chatroom', chatroom.group_name)

    # Only create new chatroom if not found
    new_chatroom = ChatGroup.objects.create(  group_name=str(shortuuid.uuid()),is_private=True)
    new_chatroom.members.add(request.user, other_user)
    new_chatroom.save()
    
    return redirect('chatroom', new_chatroom.group_name)
            
