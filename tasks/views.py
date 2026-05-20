from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from requests import get

from .models import Task

def index(request):

    if request.method == "POST":

        title = request.POST.get("title")

        if title:

            Task.objects.create(
                user_id="website",
                user_name="Website User",
                title=title
            )

        return redirect("index")

    tasks = Task.objects.all().order_by("-created_at")

    total_users = Task.objects.values("user_id").distinct().count()
    total_tasks = Task.objects.count()
    pending_tasks = Task.objects.filter(completed=False).count()
    completed_tasks = Task.objects.filter(completed=True).count()

    return render(
        request,
        "index.html",
        {
            "tasks": tasks,
            "total_users": total_users,
            "total_tasks": total_tasks,
            "pending_tasks": pending_tasks,
            "completed_tasks": completed_tasks,
        }
    )
    
    
def complete_task(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id
    )

    task.completed = True

    task.save()

    return redirect("index")

def delete_task(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id
    )

    task.delete()

    return redirect("index")