from django.shortcuts import render

def home_view(request):
    return render(request, 'home3.html')

def blog_view(request):
    return render(request,'blog-detail.html')

def blog_list_view(request):
    return render(request, 'blog-list-sidebar-left.html')

def contact_view(request):
    return render(request, 'contact.html')