from django.shortcuts import render, redirect

from apps.pages.models import ContactPagesModel


def home_view(request):
    return render(request, 'home3.html')

def blog_view(request):
    return render(request,'blog-detail.html')

def blog_list_view(request):
    return render(request, 'blog-list-sidebar-left.html')

def contact_view(request):
    if request.method == "POST":
        data = request.POST
        validated_data = {
            "full_name":data.get('full_name'),
            "email": data.get('email'),
            "subject": data.get('subject'),
            "message": data.get('message')
        }
        ContactPagesModel.objects.create(**validated_data)
        return redirect('pages:contact')
    else:
        return render(request, 'contact.html')