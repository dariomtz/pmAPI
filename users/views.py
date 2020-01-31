import json

from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from .forms import UserRegistration

def str_date(date):
    return str(date.replace(tzinfo=None, microsecond=0))

def user_model_to_json(user):
    return {
        'kind': 'user',
        'id': user.id,
        'username': user.username, 
        'first_name': user.first_name,
        'last_name': user.last_name,
        'created': str_date(user.date_joined),
    }

@csrf_exempt
def all_users(request):
    if request.method == 'POST':

        #validate input
        user = UserRegistration(json.loads(request.body))
        if not user.is_valid():
            
            response = {
                'kind' : 'error',
                'error' : json.loads(user.errors.as_json())
            }
            return HttpResponseBadRequest(json.dumps(response), content_type='application/json')

        #create new object
        model = User(**user.cleaned_data)

        #save object to database
        model.save()
        
        return JsonResponse(user_model_to_json(model))

    else:
        return HttpResponseNotAllowed(['POST'])

