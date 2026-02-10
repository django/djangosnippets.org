import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.mail import mail_admins
from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from taggit.models import Tag

from cab.forms import AdvancedSearchForm, SnippetFlagForm, SnippetForm
from cab.models import Language, Snippet, SnippetFlag
from cab.utils import month_object_list, object_detail

# Constants
MIN_QUERY_LENGTH = 2


def snippet_list(request, queryset=None, **kwargs):
    if queryset is None:
        queryset = Snippet.objects.active_snippet()

    # Handle search query
    q = request.GET.get("q", "").strip()
    if q:
        # Try PostgreSQL full-text search with ranking
        try:
            search_vector = SearchVector("title", "description", "author__username")
            search_query = SearchQuery(q)
            queryset = queryset.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by("-rank")
        except Exception:
            # Fallback to simple case-insensitive search
            queryset = queryset.filter(
                Q(title__icontains=q) | 
                Q(description__icontains=q) | 
                Q(author__username__icontains=q)
            )
        
        # Pass query to template context
        if "extra_context" not in kwargs:
            kwargs["extra_context"] = {}
        kwargs["extra_context"]["query"] = q

    if request.htmx:
        kwargs["template_name"] = "cab/partials/_snippet_table.html"

    return month_object_list(request, queryset=queryset, paginate_by=20, **kwargs)


def snippet_detail(request, snippet_id):
    return object_detail(
        request,
        queryset=Snippet.objects.all(),
        object_id=snippet_id,
        extra_context={"flag_form": SnippetFlagForm()},
    )


def download_snippet(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    response = HttpResponse(snippet.code, content_type="text/plain")
    filename = f"{snippet.id}.{snippet.language.file_extension}"
    response["Content-Disposition"] = f"attachment; filename={filename}"
    response["Content-Type"] = snippet.language.mime_type
    return response


def raw_snippet(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    response = HttpResponse(snippet.code, content_type="text/plain")
    response["Content-Disposition"] = "inline"
    return response


@login_required
def rate_snippet(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    score = request.GET.get("score")
    if score and score in ["up", "down"]:
        score = {"up": 1, "down": -1}[score]
        snippet.ratings.rate(user=request.user, score=score)
    elif score == "reset":
        snippet.ratings.unrate(request.user)
    return redirect(snippet)


@login_required
def edit_snippet(request, snippet_id=None, template_name="cab/edit_snippet.html"):
    if not request.user.is_active:
        return HttpResponseForbidden()

    if snippet_id:
        snippet = get_object_or_404(Snippet, pk=snippet_id)
        if request.user.id != snippet.author.id:
            return HttpResponseForbidden()
    else:
        template_name = "cab/add_snippet.html"
        snippet = Snippet(author=request.user, language=Language.objects.get(name="Python"))

    if request.method == "POST":
        form = SnippetForm(instance=snippet, data=request.POST)
        if form.is_valid():
            snippet = form.save()
            messages.info(request, "Your snippet has been saved")
            return redirect(snippet)
    else:
        form = SnippetForm(instance=snippet)

    return render(request, template_name, {"form": form})


@login_required
def flag_snippet(request, snippet_id, template_name="cab/flag_snippet.html"):
    snippet = get_object_or_404(Snippet, id=snippet_id)
    snippet_flag = SnippetFlag(snippet=snippet, user=request.user)

    if request.method == "POST":
        form = SnippetFlagForm(request.POST, instance=snippet_flag)

        if form.is_valid():
            snippet_flag = form.save()

            admin_link = request.build_absolute_uri(reverse("admin:cab_snippetflag_changelist"))

            mail_admins(
                f'Snippet flagged: "{snippet.title}"',
                f"{snippet_flag}\n\nAdmin link: {admin_link}",
                fail_silently=True,
            )

            messages.info(request, "Thank you for helping improve the site!")
            return redirect(snippet)
        if request.is_ajax():
            return redirect(snippet)
            messages.error(request, "Invalid form submission")
    else:
        form = SnippetFlagForm(instance=snippet_flag)
    return render(request, template_name, {"form": form, "snippet": snippet})


def author_snippets(request, username):
    user = get_object_or_404(User, username=username)
    snippet_qs = Snippet.objects.filter(author=user)
    return snippet_list(
        request,
        snippet_qs,
        template_name="cab/user_detail.html",
        extra_context={"author": user},
    )


def matches_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    snippet_qs = Snippet.objects.matches_tag(tag)
    return snippet_list(
        request,
        queryset=snippet_qs,
        template_name="cab/tag_detail.html",
        extra_context={"tag": tag},
    )


def search(request):
    query = request.GET.get("q")
    snippet_qs = Snippet.objects.none()
    if query:
        snippet_qs = (
            Snippet.objects.filter(
                Q(title__icontains=query) | Q(tags__in=[query]) | Q(author__username__iexact=query),
            )
            .distinct()
            .order_by("-rating_score", "-pub_date")
        )

    return snippet_list(
        request,
        queryset=snippet_qs,
        template_name="search/search.html",
        extra_context={"query": query},
    )


def autocomplete(request):
    q = request.GET.get("q", "")
    results = []
    if len(q) > MIN_QUERY_LENGTH:
        result_set = Snippet.objects.annotate(search=SearchVector("title")).filter(search=q)[:10]
        for obj in result_set:
            url = obj.get_absolute_url()
            results.append({"title": obj.title, "author": obj.author.username, "url": url})
    return HttpResponse(json.dumps(results), content_type="application/json")


def tag_hint(request):
    q = request.GET.get("q", "")
    results = []
    if len(q) > MIN_QUERY_LENGTH:
        tag_qs = Tag.objects.filter(slug__startswith=q)
        annotated_qs = tag_qs.annotate(count=Count("taggit_taggeditem_items__id"))

        results = [
            {"tag": obj.slug, "count": obj.count}
            for obj in annotated_qs.order_by("-count", "slug")[:10]
        ]

    return HttpResponse(json.dumps(results), content_type="application/json")


def basic_search(request):
    q = request.GET.get("q")
    snippet_qs = Snippet.objects.annotate(
        search=SearchVector("title", "description", "author__username"),
    )
    form = AdvancedSearchForm(request.GET)

    if form.is_valid():
        snippet_qs = form.search(snippet_qs)

    return snippet_list(
        request,
        queryset=snippet_qs,
        template_name="search/search.html",
        extra_context={"query": q, "form": form},
    )


def advanced_search(request):
    snippet_qs = Snippet.objects.annotate(
        search=SearchVector(
            "title",
            "description",
            "language__name",
            "version",
            "pub_date",
            "bookmark_count",
            "rating_score",
            "author__username",
        ),
    )
    form = AdvancedSearchForm(request.GET)
    if form.is_valid():
        snippet_qs = form.search(snippet_qs)

    return snippet_list(
        request,
        queryset=snippet_qs,
        template_name="search/advanced_search.html",
        extra_context={"form": form},
    )
