"""Atlas analytics trace views."""
import json
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from index.models import AnalyticsTrace, Groups, Users

from atlas.decorators import NeverCacheMixin, PermissionsCheckMixin


class Index(NeverCacheMixin, LoginRequiredMixin, TemplateView, PermissionsCheckMixin):
    template_name = "analytics/trace.html.dj"
    required_permissions = ("View Site Analytics",)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        page = int(self.request.GET.get("page", 1))
        start_at = int(self.request.GET.get("start_at", -86400))
        end_at = int(self.request.GET.get("end_at", 0))
        user_id = self.request.GET.get("user_id", -1)
        group_id = self.request.GET.get("group_id", -1)
        page_size = 10

        now = timezone.now()
        start_absolute = now + timedelta(seconds=start_at)
        end_absolute = now + timedelta(seconds=end_at)

        traces = AnalyticsTrace.objects.filter(
            access_date__gte=start_absolute, access_date__lte=end_absolute
        )

        if user_id > 0 and Users.objects.filter(user_id=user_id).exists():
            traces = traces.filter(user_id=user_id)

        if group_id > 0 and Groups.objects.filter(group_id=group_id).exists():
            traces = traces.filter(user__group__id=group_id)

        traces = traces.order_by("-access_date").all()
        paginator = Paginator(traces, page_size)

        context["unresolved"] = len(traces.exclude(handled=1))
        context["traces"] = paginator.get_page(page)

        return context

    def post(self, request, *args, **kwargs):
        trace = AnalyticsTrace.objects.filter(pk=self.kwargs["pk"])
        if trace.exists():
            trace = trace.first()
            if trace.handled == 1:
                trace.handled = None
            else:
                trace.handled = 1

            trace.save()
            return HttpResponse("Changes saved.", content_type="text/plain")
        return HttpResponse("No changes to save.", content_type="text/plain")


@login_required
@csrf_exempt
def log(request):
    """Create analytics trace."""
    log_data = json.loads(request.body.decode("utf-8"))
    for details in log_data["lg"]:
        trace = AnalyticsTrace(
            user=request.user,
            level=details["l"],
            message=details["m"],
            logger=details["n"],
            useragent=request.headers.get("User-Agent"),
            referer=request.META["HTTP_REFERER"],
            access_date=timezone.now(),
        )
        trace.save()

    return HttpResponse("ok")
