from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from .forms import NewProject, NewTask, PutProject, PatchProject
import json, datetime, uuid

projects = {}

@csrf_exempt
def all_projects(request):

    if request.method == 'GET':#get all projects
        return JsonResponse({ 'projects': projects })

    elif request.method == 'POST':#create a new project

        #validate input
        project = NewProject(json.loads(request.body))
        if not project.is_valid():
            response = {
                'kind': 'error',
                'errors': json.loads(project.errors.as_json())
            }
            return HttpResponseBadRequest(json.dumps(response), content_type='application/json')
        
        #creation of new object
        body = project.cleaned_data
        id = str(uuid.uuid4())
        new_project = {
            'kind': 'project',
            'id': id,
            'title': body['title'], 
            'description': body['description'],
            'created': str(datetime.datetime.now()),
            'updated': str(datetime.datetime.now()),
            'canRead':[],
            'canEdit':[],
            'admins':[],
            'tasks': {},
            'deadline': str(body['deadline'].replace(tzinfo=None)) if 'deadline' in body and body['deadline'] != None else None,
            'status': 0,
        }

        #Save changes in database
        projects[id] = new_project

        return JsonResponse(new_project)
    
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

@csrf_exempt
def specific_project(request, projectId=None):

    #Validate that the project exists
    if not str(projectId) in projects:
        response = {
                'kind': 'error',
                'errors': {
                    'request':{
                        'message': 'A project with that id does not exist.',
                        'code': 'not found'
                    }
                }
            }
        return HttpResponseNotFound(json.dumps(response) , content_type='application/json')

    if request.method == 'GET':#gets the specific project
        return JsonResponse(projects[str(projectId)])
        
    elif request.method == 'POST':#post a task to the project
        
        #validate input
        task = NewTask(json.loads(request.body))
        if not task.is_valid():
            response = {
                'kind': 'error',
                'errors': json.loads(task.errors.as_json())
            }
            return HttpResponseBadRequest(json.dumps(response) , content_type='application/json')

        #creation of new object
        body = task.cleaned_data
        id = str(uuid.uuid4())
        new_task = {
            'kind': 'task',
            'id': id,
            'title': body['title'], 
            'description': body['description'],
            'created': str(datetime.datetime.now()),
            'updated': str(datetime.datetime.now()),
            'deadline': str(body['deadline'].replace(tzinfo=None)) if 'deadline' in body and body['deadline'] != None else None,
            'startDate': str(body['startDate'].replace(tzinfo=None)) if 'startDate' in body and body['startDate'] != None else None,
            'inCharge':[],
            'resources': body['resources'] if 'resources' in body else None,
            'status': 0,
        } 

        #Save changes in database
        projects[str(projectId)]['tasks'][id] = new_task

        return JsonResponse(new_task)

    elif request.method == 'PUT':#modify the entire project to these new values
        
        #validate input
        project = PutProject(json.loads(request.body))
        if not project.is_valid():
            response = {
                'kind': 'error',
                'errors': json.loads(project.errors.as_json())
            }
            return HttpResponseBadRequest(json.dumps(response), content_type='application/json')

        #creation of new object
        body = project.cleaned_data
        id = str(projectId)
        modified_project = {
            'kind': 'project',
            'id': id,
            'title': body['title'], 
            'description': body['description'],
            'created': projects[id]['created'],
            'updated': str(datetime.datetime.now()),
            'canRead': [],
            'canEdit': [],
            'admins': [],
            'tasks': projects[id]['tasks'],
            'deadline': str(body['deadline'].replace(tzinfo=None)),
            'status': body['status'],
        }

        #save changes in database
        projects[id] = modified_project

        return JsonResponse(modified_project)

    elif request.method == 'PATCH':#modify only the changes to the resource

        #validate input
        project = PatchProject(json.loads(request.body))
        if not project.is_valid():
            response = {
                'kind': 'error',
                'errors': json.loads(project.errors.as_json())
            }
            return HttpResponseBadRequest(json.dumps(response), content_type='application/json')

        #creation of new object
        body = project.cleaned_data
        id = str(projectId)
        modified_project = {
            'kind': 'project',
            'id': id,
            'title': body['title'] if 'title' in body else projects[id]['title'], 
            'description': body['description'] if 'description' in body else projects[id]['description'],
            'created': projects[id]['created'],
            'updated': str(datetime.datetime.now()),
            'canRead': [],
            'canEdit': [],
            'admins': [],
            'tasks': projects[id]['tasks'],
            'deadline': str(body['deadline'].replace(tzinfo=None)) if 'deadline' in body and body['deadline'] != None else projects[id]['deadline'],
            'status': body['status'] if 'status' in body else projects[id]['status'],
        }

        #save changes in database
        projects[id] = modified_project

        return JsonResponse(modified_project)

    elif request.method == 'DELETE':#deletes the project
        del projects[str(projectId)]
        return HttpResponse(status=204)

    else:
        return HttpResponseNotAllowed(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])