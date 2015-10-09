from django.shortcuts import render_to_response
from webportal.app.models import TaskTable


def index(request):
    task_table = TaskTable()
    task_table.Name = '123'
    task_table._request = request
    task_table.save()

    return render_to_response('main.html', {'test': 'test value'})
