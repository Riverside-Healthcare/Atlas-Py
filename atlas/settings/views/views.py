"""Atlas settings."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from atlas.decorators import NeverCacheMixin, PermissionsCheckMixin


class Index(NeverCacheMixin, LoginRequiredMixin, PermissionsCheckMixin, TemplateView):
    template_name = "settings/index.html.dj"
    required_permissions = ("Manage Global Site Settings",)

    def get_context_data(self, **kwargs):
        """Add context to request."""
        context = super().get_context_data(**kwargs)
        context["title"] = "Settings"

        return context
