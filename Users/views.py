from django.shortcuts import get_object_or_404, redirect, render
# Create your views here.
import shutil
from django.shortcuts import render
from .models import Block, userRegisteredTable
from django.core.exceptions import ValidationError
from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.db import IntegrityError
from .models import userRegisteredTable, Block
from .blockchain import Blockchain, Block as BlockchainBlock
from django.contrib import messages

# Module-level Blockchain instance with the stable AES key
blockchain = Blockchain()


def Ulog(request):
    request.session.flush()  # clears all session data
    return render(request, 'userLoginForm.html')


def userRegisterCheck(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        username = request.POST.get("username", "").strip()
        mobile = request.POST.get("mobile", "").strip()
        password = request.POST.get("password", "")

        profile_picture = request.FILES.get("profile_picture")

        form_data = {
            "name": name,
            "email": email,
            "username": username,
            "mobile": mobile,
        }

        if userRegisteredTable.objects.filter(email__iexact=email).exists():
            return render(request, "userRegisterForm.html", {
                "messages": ["Email already exists. Please use another email or log in."],
                "form_data": form_data,
            })

        if userRegisteredTable.objects.filter(loginid__iexact=username).exists():
            return render(request, "userRegisterForm.html", {
                "messages": ["Username already exists. Please choose another username."],
                "form_data": form_data,
            })

        user = userRegisteredTable(
            name=name,
            email=email,
            loginid=username,
            mobile=mobile,
            password=password,
            profile_picture=profile_picture
        )

        try:
            user.full_clean()
            user.save()
            messages.success(request, 'Registration successfully done, please wait for admin approval.')
            return render(request, "userRegisterForm.html")

        except ValidationError as ve:
            field_labels = {
                "name": "Full name",
                "email": "Email",
                "loginid": "Username",
                "mobile": "Mobile",
                "password": "Password",
            }
            error_messages = []
            for field, errors in ve.message_dict.items():
                for error in errors:
                    error_messages.append(f"{field_labels.get(field, field.capitalize())}: {error}")
            return render(request, "userRegisterForm.html", {
                "messages": error_messages,
                "form_data": form_data,
            })

        except IntegrityError:
            return render(request, "userRegisterForm.html", {
                "messages": ["This email or username is already registered."],
                "form_data": form_data,
            })

        except Exception as e:
            return render(request, "userRegisterForm.html", {
                "messages": [str(e)],
                "form_data": form_data,
            })

    return render(request, "userRegisterForm.html")


def userLoginCheck(request):
    if request.method == 'POST':
        username = request.POST['userUsername']
        password = request.POST['userPassword']
        try:
            user = userRegisteredTable.objects.get(loginid=username, password=password)
            if user.status == 'Active':
                request.session.flush()         # ← Clear any previous session first
                request.session['id'] = user.id
                request.session['name'] = user.name
                request.session['email'] = user.email
                request.session['loginid11'] = user.loginid
                return render(request, 'users/userHome.html', {
                    'name': user.name,           # ← Pass explicitly, don't rely on template reading session
                    'loginid': user.loginid,
                })
            else:
                messages.error(request, 'Status not activated, please wait for admin approval')
                return render(request, 'userLoginForm.html')
        except:
            messages.error(request, 'Invalid details')
            return render(request, 'userLoginForm.html')
    return render(request, 'userLoginForm.html')

def userHome(request):
    if not request.session.get('id'):
        return render(request, 'userLoginForm.html')
    return render(request, 'users/userHome.html')


def search(request):
    if not request.session.get('id'):
        return render(request, 'userLoginForm.html')
    if request.method == "POST":
        username = request.POST['username']
        try:
            current_user_loginid = request.session.get('loginid11')

            # Case-insensitive search
            userss = userRegisteredTable.objects.filter(
                loginid__iexact=username, status='Active'
            ).exclude(loginid__iexact=current_user_loginid)

            if userss:
                return render(request, 'users/search.html', {'users': userss})
            else:
                # Check if user exists but is NOT yet activated
                pending = userRegisteredTable.objects.filter(
                    loginid__iexact=username
                ).exclude(loginid__iexact=current_user_loginid).first()

                if pending:
                    messages.error(
                        request,
                        f'User "{pending.loginid}" exists but is not yet activated by admin. '
                        f'Please ask the admin to activate this account first.'
                    )
                elif username.lower() == (current_user_loginid or '').lower():
                    messages.error(request, 'You cannot search for yourself!')
                else:
                    messages.error(request, f'No active user found with username "{username}".')
                return render(request, 'users/search.html')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return render(request, 'users/search.html')
    return render(request, 'users/search.html')


def _load_messages(sender, recipient_loginid):
    """Helper: fetch and decrypt all messages between sender and recipient."""
    blocks = Block.objects.all().order_by('timestamp')
    result = []
    for block in blocks:
        try:
            decrypted = BlockchainBlock.decrypt_message(block.message, blockchain.encryption_key)
            if (
                (block.sender == sender and block.recipient == recipient_loginid) or
                (block.sender == recipient_loginid and block.recipient == sender)
            ):
                result.append({
                    'sender': block.sender,
                    'message': decrypted,
                    'timestamp': block.timestamp,
                })
        except Exception as e:
            print(f"Decryption error for block {block.id}: {e}")
            continue
    return result


def start_chat(request):
    # Must be logged in
    if not request.session.get('id'):
        return redirect('userLoginForm')

    sender = request.session.get('loginid11')

    if request.method == "GET":
        loginid = request.GET.get('username', '')
        if not loginid:
            messages.error(request, 'No recipient specified.')
            return redirect('search')

        # Prevent self-chat
        if loginid == sender:
            messages.error(request, 'You cannot chat with yourself!')
            return redirect('search')

        recipient = get_object_or_404(userRegisteredTable, loginid=loginid, status='Active')
        messagesss = _load_messages(sender, recipient.loginid)

        return render(request, 'users/start_chat.html', {
            'recipient': recipient,
            'messagesss': messagesss,
            'sender': sender,
        })

    elif request.method == 'POST':
        loginid = request.POST.get('username', '')
        message1 = request.POST.get('message', '').strip()

        if not loginid:
            messages.error(request, 'Recipient not found.')
            return redirect('search')

        # Prevent self-chat
        if loginid == sender:
            messages.error(request, 'You cannot chat with yourself!')
            return redirect('search')

        recipient = get_object_or_404(userRegisteredTable, loginid=loginid, status='Active')

        if message1:
            try:
                new_block = blockchain.add_block(sender, recipient.loginid, message1)
                Block.objects.create(
                    index=new_block.index,
                    sender=new_block.sender,
                    recipient=new_block.recipient,
                    message=new_block.message,
                    timestamp=new_block.timestamp,
                    previous_hash=new_block.previous_hash,
                    hash=new_block.hash,
                    nonce=new_block.nonce,
                )
                messages.success(request, 'Message sent!')
            except Exception as e:
                messages.error(request, f'Failed to send message: {str(e)}')

        else:
            messages.error(request, 'Message cannot be empty.')

        from django.urls import reverse
        return redirect(f"{reverse('start_chat')}?username={recipient.loginid}")

    return redirect('search')


def clear_blocks(request):
    """Admin-only utility: wipe all Block records so chats start fresh."""
    if not request.session.get('id'):
        return redirect('userLoginForm')
    if request.method == 'POST':
        deleted_count, _ = Block.objects.all().delete()
        messages.success(request, f'Cleared {deleted_count} old block records. Chat history reset!')
    return render(request, 'users/clear_blocks.html')


def chatHistory(request):
    return render(request, 'users/chatHistory.html')
