from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def all_users(request):
    return JsonResponse({'it': 'works'})

