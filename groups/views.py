import datetime
import json

from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotAllowed, HttpResponseNotFound,
                         JsonResponse)
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def groups_view(request):
    return JsonResponse({})