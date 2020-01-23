from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from .forms import ProjectForm, TaskForm
from .models import Project, Task
import json, datetime, uuid

projects = {}

def str_date(date):
    return str(date.replace(tzinfo=None))

def json_query_set(QuerySet):
    json = {}
    for model in list(QuerySet.values()):
        model['deadline'] = str_date(model['deadline'])
        model['created'] = str_date(model['created'])
        model['updated'] = str_date(model['updated'])
        json[model['id']] = model
    return json

def list_query_set(QuerySet):
    query_list =list(QuerySet.values())
    for model in query_list:
        model['deadline'] = str_date(model['deadline'])
        model['created'] = str_date(model['created'])
        model['updated'] = str_date(model['updated'])
    return query_list

@csrf_exempt
def all_projects(request):

    if request.method == 'GET':#get all projects
        return JsonResponse({ 'projects': list_query_set(Project.objects.all()) })

    elif request.method == 'POST':#create a new project

        #validate input
        project = ProjectForm(json.loads(request.body))
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
                    'request':[
                        {
                        'message': 'A project with that id does not exist.',
                        'code': 'not found'
                        }
                    ]
                        
                }
            }
        return HttpResponseNotFound(json.dumps(response) , content_type='application/json')

    if request.method == 'GET':#gets the specific project
        return JsonResponse(projects[str(projectId)])
        
    elif request.method == 'POST':#post a task to the project
        
        #validate input
        task = TaskForm(json.loads(request.body))
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
        project = ProjectForm(json.loads(request.body))
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

    elif request.method == 'DELETE':#deletes the project
        del projects[str(projectId)]
        return HttpResponse(status=204)

    else:
        return HttpResponseNotAllowed(['GET', 'POST', 'PUT', 'DELETE'])

def specific_task(request, projectId=None, taskId=None):

    #validate that the project and task both exist
    if not str(projectId) in projects or not str(taskId) in projects[str(projectId)]['tasks']:
        response = {
                'kind': 'error',
                'errors': {
                    'request':[
                        {
                        'message': 'A project or task with that id does not exist.',
                        'code': 'not found'
                        }
                    ]
                        
                }
            }
        return HttpResponseNotFound(json.dumps(response) , content_type='application/json')

    if request.method == 'GET': 
        return JsonResponse(projects[str(projectId)]['tasks'][str(taskId)])

    if True:
        return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])