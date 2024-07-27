from django.shortcuts import render


def index(request):
    test_data = {"test": "this is str from server"}

    return render(request, 'index.html', test_data)
