from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from cab.models import Bookmark, Snippet
from cab.utils import object_list


@login_required
def user_bookmarks(request):
    return object_list(
        request,
        queryset=Bookmark.objects.filter(user__pk=request.user.id),
        template_name='cab/user_bookmarks.html',
        paginate_by=20)


@login_required
def add_bookmark(request, snippet_id):
    # TODO: this should probably be a POST action
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    try:
        Bookmark.objects.get(user=request.user,
                             snippet=snippet)
    except Bookmark.DoesNotExist:
        Bookmark.objects.create(user=request.user,
                                snippet=snippet)
    return redirect(snippet)


@login_required
def delete_bookmark(request, snippet_id):
    bookmark = get_object_or_404(Bookmark,
                                 snippet__pk=snippet_id,
                                 user=request.user)
    if request.method == 'POST':
        bookmark.delete()
        return redirect(bookmark.snippet)
    else:
        return render(request, 'cab/confirm_bookmark_delete.html',
                      {'snippet': bookmark.snippet})
