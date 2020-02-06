import datetime
import json

from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotAllowed, HttpResponseNotFound,
                         JsonResponse)
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def groups_view(request):
    return JsonResponse({})

def single_group_view(request, groupId=None):
    return JsonResponse({})

def add_project_group(request,groupId=None):
    return JsonResponse()