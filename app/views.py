from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from todoist.api import TodoistAPI
import json


def initials(request):
    res = requests.post(
        url='https://app.asana.com/api/1.0/webhooks',
        headers={"Authorization": "Bearer 0/92f79995f7c1b4b0f751b9a07c8e52c2"},
        data={"resource": "1116265931583433", "target": "http://127.0.0.1:8000/payload/"}
    )


def handle_payload(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)

        if 'events' in received_json_data.keys():
            events = received_json_data["events"]

            for event in events:
                id = event["resource"]
                type = event["type"]
                url = None
                if type == "task":
                    url = "https://app.asana.com/api/1.0/tasks/" + str(id)

                if not url == None:
                    data = requests.get(
                        url=url,
                        headers={"Authorization": "Bearer 0/92f79995f7c1b4b0f751b9a07c8e52c2"}
                    )

                    data1 = json.loads(data)
                    if data1['data']['assignee']['name']=='Yukta Anand':
                        task_name = data1['data']['name']
                        api = TodoistAPI('27113e1797906a73a11a7358805ac473499c414e')
                        api.sync()
                        project_name = data1['data']['memberships']['project']['name']
                        project1 = api.projects.add(project_name)
                        api.items.add(task_name, project1['id'])
                        api.commit()
        else:
            headers = request.headers
            x_hook = headers['X-Hook-Secret']
            return JsonResponse({"X-Hook-Secret": x_hook})

