from django.urls import path

from cab.views import bookmarks

urlpatterns = [
    path("", bookmarks.user_bookmarks, name="cab_user_bookmarks"),
    path("add/<int:snippet_id>/", bookmarks.add_bookmark, name="cab_bookmark_add"),
    path(
        "delete/<int:snippet_id>/",
        bookmarks.delete_bookmark,
        name="cab_bookmark_delete",
    ),
]
