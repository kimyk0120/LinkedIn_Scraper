import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .core import person as core_person
from .core import company_person as core_company


# test
def hello(request):
    test_data = {"test": "this is str from server"}
    return render(request, 'hello.html', test_data)


# main index
def index(request):
    return render(request, 'index.html')


@csrf_exempt
def scrape(request):
    if request.method == 'POST':

        # get parameters from request body
        request_body = request.body.decode('utf-8')
        req_json_data = json.loads(request_body)
        print("req_json_data: ", req_json_data)

        url = req_json_data['url']
        select_val = req_json_data['select']

        if not url:
            return JsonResponse({"error": "Invalid request body"}, status=400)

        if select_val == 'company':
            jsonData = core_company.scraper_from_company(url)
        else:
            jsonData = core_person.scraper(url)

        return JsonResponse(jsonData)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)
