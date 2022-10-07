"""Atlas ETL for Search."""
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache

from ..tasks.search.groups import reset_groups as task_reset_groups
from . import build_task_status, toggle_task_status


@never_cache
def groups(request, arg):
    """Search ETL for groups.

    options:
        status: returns enabled/disabled status of ETL
        enable: enables the etl
        disable: disables the etl
        trigger: runs the etl
    """
    task_name = "search groups"
    task_function = "etl.tasks.search.groups.reset_groups"

    if arg == "status":
        return JsonResponse(build_task_status(task_name, task_function))

    elif arg in ["enable", "disable"]:
        return JsonResponse(
            {"message": toggle_task_status(task_name, task_function, arg)}
        )

    elif arg == "run":
        # Reload groups now.
        task_reset_groups.delay()

        return redirect("/etl")

    return JsonResponse({"status": "error"})
