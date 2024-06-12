from django.shortcuts import render


def index(request):
    return render(request, 'home/index.html')


def blog(request):
    return render(request, 'home/blog.html')


def contact(request):
    return render(request, 'home/contact.html')


def pricing(request):
    return render(request, 'home/pricing.html')


def features(request):
    return render(request, 'home/features.html')


def privacy(request):
    return render(request, 'home/privacy.html')

