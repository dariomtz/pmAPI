from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json, datetime

projects = {
    '1':{
        'title': 'Dummy Project',
        'id': '1',
        'description': 'This is a project to test the feature that creates projects',
        'user': 'Dario Martinez',
        'created': '2011-08-01T19:58:51.947',
        'updated': '2011-08-01T19:58:51.947',
        'kind': 'project'
    }
}

@csrf_exempt
def projectHandler(request):
    if request.method == 'GET':
        response = { 'projects': projects }
        return JsonResponse(response)

    elif request.method == 'POST':
        body = json.loads(request.body)

        #validation
        if not 'title' in body:
            return HttpResponseBadRequest('A project cannot be created without title')
        if not 'description' in body:
            return HttpResponseBadRequest('A project cannot be created without description')

        #creation of new object
        id = str(len(projects) + 1)
        newProject = {
            'title': body['title'],
            'description': body['description'],
            'user': 'Default user',
            'id': id,
            'created': datetime.datetime.now(),
            'updated': datetime.datetime.now(),
            'kind': 'project'
        }
        projects[id] = newProject
        return JsonResponse(newProject)

        