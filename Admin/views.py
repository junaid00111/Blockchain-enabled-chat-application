from django.shortcuts import render
from django.contrib import messages

from Users.models import Block, userRegisteredTable


def adminHome(request):
    if not request.session.get('admin'):
        return render(request,'amdinLoginForm.html')
    return render(request,'admin/adminHome.html')

def adminLoginCheck(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        if password=="admin" and username=='admin':
            request.session['admin']=True
            return render(request,'admin/adminHome.html')
        else:
            messages.error(request,'Invalid details,please enter details carefully')
            return render(request,'adminLoginForm.html')
        
    return render(request,'adminLoginForm.html')

def userList(request):
    if not request.session.get('admin'):
        return render(request,'adminLoginForm.html') 
    users=userRegisteredTable.objects.all()
    return render(request,'admin/userList.html',{'users':users})


def log(request):
    request.session.flush()  # clears all session data
    return render(request,'adminLoginForm.html')





from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

def activate_user(request):
    if not request.session.get('admin'):
        return render(request,'adminLoginForm.html') 

    id=request.GET['id']
    user = get_object_or_404(userRegisteredTable, id=id)
    user.status = 'Active'
    user.save()
    users=userRegisteredTable.objects.all()
    return render(request,'admin/userList.html',{'users':users})  

def deactivate_user(request):
    if not request.session.get('admin'):
        return render(request,'adminLoginForm.html') 
    
    id=request.GET['id']
    user = get_object_or_404(userRegisteredTable, id=id)
    user.status = 'Inactive'
    user.save()
    users=userRegisteredTable.objects.all()
    return render(request,'admin/userList.html',{'users':users})

def delete_user(request):
    if not request.session.get('admin'):
        return render(request,'adminLoginForm.html')

    id = request.GET['id']
    user = get_object_or_404(userRegisteredTable, id=id)
    loginid = user.loginid
    Block.objects.filter(sender=loginid).delete()
    Block.objects.filter(recipient=loginid).delete()
    user.delete()
    messages.success(request, f'{loginid} has been deleted.')
    return redirect('userList')

