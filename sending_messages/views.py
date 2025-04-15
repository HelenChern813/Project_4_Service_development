from django.shortcuts import render


def base_view(request):
    return render(request, 'sending_messages/base.html')
