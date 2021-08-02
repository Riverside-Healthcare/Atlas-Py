"""Atlas Term views."""
# pylint: disable=C0116,C0115,W0613,W0212

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.generic import DetailView, ListView, View
from index.models import (
    CollectionTerms,
    Reports,
    ReportTerms,
    TermComments,
    TermCommentStream,
    Terms,
)

decorators = [never_cache, login_required]


@login_required
def delete(request, pk):
    """Delete a term.

    1. comments
    2. comment streams
    3. report doc term links
    4. collection annotations
    5. term
    """
    TermComments.objects.filter(stream_id__term_id=pk).delete()
    TermCommentStream.objects.filter(term_id=pk).delete()
    ReportTerms.objects.filter(term__term_id=pk).delete()
    CollectionTerms.objects.filter(term__term_id=pk).delete()
    get_object_or_404(Terms, pk=pk).delete()

    return redirect("term:list")


class TermList(LoginRequiredMixin, ListView):
    queryset = Terms.objects.order_by("-approved", "-_modified_at")
    context_object_name = "terms"
    template_name = "terms.html.dj"
    extra_context = {"title": "Terms"}

    def get(self, request, **kwargs):
        if request.GET.get("id"):
            return redirect("/terms/%s" % request.GET.get("id"))

        return super().get(request, **kwargs)


class TermDetails(LoginRequiredMixin, DetailView):
    template_name = "term.html.dj"
    context_object_name = "term"
    queryset = (
        Terms.objects.select_related("approved_by")
        .select_related("modified_by")
        .prefetch_related("report_docs")
        .prefetch_related("report_docs__report_doc")
        .prefetch_related("report_docs__report_doc__report")
        .prefetch_related("collections")
        .prefetch_related("collections__collection")
        .prefetch_related("collections__collection__initiative")
    )

    def get_context_data(self, **kwargs):
        """Add additional items to the context."""
        context = super().get_context_data(**kwargs)

        term_id = self.kwargs["pk"]

        context["related_reports"] = (
            Reports.objects.filter(
                # link ed terms
                Q(docs__terms__term_id=term_id)
                |
                # parent linked terms
                Q(parent__child__docs__terms__term_id=term_id)
                |
                # grandparent linked terms
                Q(parent__child__parent__child__docs__terms__term_id=term_id)
                |
                # great grandparent linked terms
                # pylint: disable=C0301
                Q(
                    parent__child__parent__child__parent__child__docs__terms__term_id=term_id  # noqa: E501
                )
            )
            .filter(Q(docs__hidden="N") | Q(docs__hidden__isnull=True))
            .filter(visible="Y")
        ).distinct()

        context["title"] = self.object.name
        context["favorite"] = (
            "favorite" if self.request.user.has_favorite("term", term_id) else ""
        )

        return context

    def post(self, request, **kwargs):
        term = Terms.objects.get(term_id=self.kwargs["pk"])
        term.name = request.POST.get("name", "")
        term.summary = request.POST.get("summary", "")
        term.technical_definition = request.POST.get("technical_definition", "")

        if term.approved != "Y" and request.POST.get("approved", "N") == "Y":
            # add date if term is now approved
            term._approved_at = timezone.now()

        elif term.approved == "Y" and request.POST.get("approved", "N") == "N":
            # remove date it term is now not approved
            term._approved_at = None

        term.approved = request.POST.get("approved", "N")
        term.external_standard_url = request.POST.get("external_standard_url", "")
        term._valid_from = request.POST.get("valid_from", "") or None
        term.modified_by = request.user

        term.save()

        return redirect("term:details", **kwargs)


class TermNew(LoginRequiredMixin, View):
    def post(self, request):
        term = Terms(
            name=request.POST.get("name", ""),
            summary=request.POST.get("summary", ""),
            technical_definition=request.POST.get("technical_definition", ""),
            approved=request.POST.get("approved", "N"),
            external_standard_url=request.POST.get("external_standard_url", ""),
            _valid_from=(request.POST.get("valid_from", "") or None),
            modified_by=request.user,
        )

        if request.POST.get("approved", "N") == "Y":
            term._approved_at = timezone.now()

        term.save()

        return redirect("term:details", pk=term.term_id)

    def get(self, request):
        return redirect("term:list")
