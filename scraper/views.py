from django.shortcuts import render


# test
def hello(request):
    test_data = {"test": "this is str from server"}
    return render(request, 'hello.html', test_data)


# main index
def index(request):
    return render(request, 'index.html')
