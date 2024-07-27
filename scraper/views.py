from django.shortcuts import render


def hello(request):
    test_data = {"test": "this is str from server"}
    return render(request, 'hello.html', test_data)


def index(request):
    return render(request, 'index.html')
