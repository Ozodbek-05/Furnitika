from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils import timezone

from apps.pages.forms import ContactForm
from apps.pages.models import BannerModel
from apps.products.models import DealOfTheDayModel


def home_view(request):
    banners = BannerModel.objects.all()
    now = timezone.now()
    deals = DealOfTheDayModel.objects.filter(
        start_time__lte=now,
        end_time__gte=now
    ).select_related("product")


    deals_list = list(deals)
    if deals_list:
        deals_list = deals_list * 3

    context = {
        'deals': deals_list,
        'banners': banners
    }
    return render(request, 'pages/home3.html', context)


def contact_page_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message sent successfully!")
            return redirect('pages:contact')
        else:
            return render(request, 'pages/contact.html', {'errors': form.errors})
    else:
        return render(request, 'pages/contact.html')

def about_view(request):
    return render(request, 'pages/about-us.html')

def not_found_view(request, exception=None):
    return render(request, 'pages/404.html', status=404)

