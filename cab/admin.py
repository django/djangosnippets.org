from django.contrib import admin

from cab.models import Language, Snippet


class LanguageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}


class SnippetAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'rating_score', 'pub_date')
    list_filter = ('language',)
    date_hierarchy = 'pub_date'
    search_fields = ('author__username', 'title', 'description', 'code',)


admin.site.register(Language, LanguageAdmin)
admin.site.register(Snippet, SnippetAdmin)
