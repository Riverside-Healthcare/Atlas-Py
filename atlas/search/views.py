"""Atlas Search."""
import copy

import pysolr
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from index.models import Projects


@login_required
def template(request):
    """Return search template.

    This view is public and requires no auth.
    """
    return render(None, "template.html")


@login_required
def index(request, search_type="query", search_string=""):
    """Atlas Search.

    - search requests data from solr
    - get users permissions and favorites
    - modify json
        - add "favorite" column
        - add run url, based on permissions
        - adds project ads

    Still need to add facet ranges

    """
    reserved_characters = (
        "\\",
        "+",
        "-",
        "&&",
        "||",
        "!",
        "(",
        ")",
        "{",
        "}",
        "[",
        "]",
        "^",
        '"',
        "~",
        "*",
        "?",
        ":",
        "/",
    )

    if request.method == "GET":
        context = {
            "permissions": request.user.get_permissions(),
            "user": request.user,
            "favorites": request.user.get_favorites(),
        }

        return render(request, "search.html.dj", context)

    request_dict = dict(request.GET)

    # create a solr instance, based on the search type.
    solr = pysolr.Solr(
        settings.SOLR_URL, search_handler=search_type.replace("terms", "aterms")
    )

    # clean search string
    for char in reserved_characters:
        search_string = (
            search_string.replace(char, "\\%s" % char)
            if char in search_string
            else search_string
        )

    # build the solr search string
    # pylint: disable=C0301
    search_string = "name:({search})^4 OR name:*({search})*^3 OR ({search})^2 OR *({search})*~".format(  # noqa: E501
        search=search_string
    )

    # build solr fq (filter query)
    filter_query = build_filter_query(request_dict.items())

    # add visibility filter - by default only showing visible reports
    if request_dict.get("visibility_text", "Y") == ["Y"]:
        filter_query.append("{!tag=visibility_text}visibility_text:Y")
    else:
        filter_query.append(
            "{!tag=visibility_text}visibility_text:Y OR {!tag=visibility_text}visibility_text:N"
        )

    # pagination
    start = request_dict.get("start", [0])[0]

    # pylint: disable=C0301
    results = solr.search(
        search_string,
        fq=(",".join(filter_query)),
        rq="{!rerank reRankQuery=$rqq reRankDocs=1000 reRankWeight=10}",
        rqq='(documented:1 OR executive_visibility_text:Y OR enabled_for_hyperspace_text:Y OR certification_text:"Analytics Certified")',  # noqa: E501
        start=start,
    )

    output = {
        "docs": results.docs,
        "stats": results.stats.get("stats_fields", {})
        if hasattr(results, "stats")
        else "",
        "facets": {},
        "hits": results.hits,
        "start": start,
    }

    if hasattr(results, "facets"):
        output["facets"] = copy.deepcopy(results.facets)
        for attr, value in results.facets.get("facet_fields").items():
            if value:
                output["facets"]["facet_fields"][attr] = {}

                fields = results.facets.get("facet_fields").get(attr)
                for num, field in enumerate(fields[::2]):
                    output["facets"]["facet_fields"][attr][field] = fields[
                        (num * 2) + 1
                    ]

    # pass back search filters
    output["search_filters"] = {"type": search_type or "query"}

    for key, values in request_dict.items():
        output["search_filters"][key] = values

    # get project from results.. if not searching projects
    if search_type != "projects":
        term_ids = []
        report_ids = []

        for doc in results.docs:
            if doc.get("type")[0] == "reports":
                report_ids.append(doc.get("atlas_id")[0])
            elif doc.get("type")[0] == "terms":
                term_ids.append(doc.get("atlas_id")[0])

        # get projects from results
        projects = (
            Projects.objects.filter(
                Q(term_annotations__term__term_id__in=term_ids)
                | Q(report_annotations__report__report_id__in=report_ids)
            )
            .filter(Q(hidden__isnull=True) | Q(hidden="N"))
            .all()
            .values("project_id", "purpose", "description", "name")
            .distinct()
        )

        output["projects"] = list(projects)

    return JsonResponse(output, safe=False)


def build_filter_query(request_items):
    """Build filter query from items."""
    filter_query = []
    for key, values in request_items:
        # it is possible to have multiple filters
        # per field
        if key != "visibility_text" and key != "start":
            filter_query.append(
                "%s"
                % " OR ".join(
                    "{!tag=%s}%s:%s"
                    % (
                        key,
                        key,
                        value,
                    )
                    for value in values
                )
            )

    return filter_query


@login_required
def lookup(request, lookup):
    """Mini search for dropdowns."""
    my_json = {"lookup": lookup}
    return JsonResponse(my_json, safe=False)
