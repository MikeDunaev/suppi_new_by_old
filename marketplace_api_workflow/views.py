# from django.shortcuts import render
from django.http import JsonResponse

from marketplace_api_workflow import services


def index(request):
    #print(request.META) # CGI-like headers
    return JsonResponse({'success': True})
