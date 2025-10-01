# pages/views.py
from django.shortcuts import redirect, render
from django.utils import timezone

from apps.pages.forms import ContactForm
from apps.products.models import DealOfTheDayModel   # product appdan import qilamiz


def home_view(request):
    deal = (
        DealOfTheDayModel.objects
        .filter(start_time__lte=timezone.now(), end_time__gte=timezone.now())
        .select_related("product")
        .first()
    )
    return render(request, 'pages/home3.html', {"deal": deal})


def contact_page_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            context = {
                'errors': form.errors
            }
            return render(request, 'pages/contact.html', context)
        return redirect('pages:contact')
    else:
        return render(request, 'pages/contact.html')


def about_view(request):
    return render(request, 'pages/about-us.html')


def not_found_view(request, exception=None):
    return render(request, 'pages/404.html', status=404)
