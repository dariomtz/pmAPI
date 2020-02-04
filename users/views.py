import json

from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .forms import UserRegistration, UserLogin

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

    if request.method == 'GET':

        try:
            user = User.objects.get(username=request.user)
            response = user_model_to_json(user)
        except:
            response = {
                    'kind': 'error',
                    'errors': {
                        'request':[
                            {
                            'message': 'You are not logged in.',
                            'code': 'auth'
                            }
                        ]
                            
                    }
                }
            return HttpResponseNotFound(json.dumps(response) , content_type='application/json')

        else:
            return JsonResponse(response)

    elif request.method == 'POST':

        #validate input
        user = UserRegistration(json.loads(request.body))
        if not user.is_valid():
            
            response = {
                'kind' : 'error',
                'errors' : json.loads(user.errors.as_json())
            }
            return HttpResponseBadRequest(json.dumps(response), content_type='application/json')

        #create new object
        model = User(**user.cleaned_data)

        #save object to database
        model.save()
        
        return JsonResponse(user_model_to_json(model))

    else:
        return HttpResponseNotAllowed(['POST', 'GET'])

@csrf_exempt
def login_user(request):

    if request.method == 'POST':

        form = UserLogin(json.loads(request.body))

        if not form.is_valid():
            response = {
                'kind' : 'error',
                'error' : json.loads(form.errors.as_json())
            }
            return HttpResponseBadRequest(json.dumps(response), content_type='application/json')

        print(form.cleaned_data['username'], form.cleaned_data['password'])

        user = authenticate(request=request, username= form.cleaned_data['username'], password= form.cleaned_data['password'])
        print(user)
        if user is not None:
            login(request, user)
            return HttpResponse(status='204')
        else:
            response = {
                    'kind': 'error',
                    'errors': {
                        'request':[
                            {
                            'message': 'Username or password not correct.',
                            'code': 'invalid'
                            }
                        ]
                            
                    }
                }
            return HttpResponseBadRequest(json.dumps(response) , content_type='application/json')

    else:
        return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def logout_user(request):
    if request.method == 'GET':
        logout(request)
        return HttpResponse(status='204')
    else:
        return HttpResponseNotAllowed(['GET'])
