from django.contrib import admin

from cab.models import Language, Snippet, SnippetFlag


class LanguageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}


class SnippetAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'rating_score', 'pub_date')
    list_filter = ('language',)
    date_hierarchy = 'pub_date'
    search_fields = ('author__username', 'title', 'description', 'code',)


class SnippetFlagAdmin(admin.ModelAdmin):
    list_display = ('snippet', 'flag')
    list_filter = ('flag',)
    
    actions = ['remove_and_ban']
    
    def remove_and_ban(self, request, queryset):
        for obj in queryset:
            obj.remove_and_ban()
        self.message_user(request, 'Snippets removed successfully')
    remove_and_ban.short_description = 'Remove snippet and ban user'


admin.site.register(Language, LanguageAdmin)
admin.site.register(Snippet, SnippetAdmin)
admin.site.register(SnippetFlag, SnippetFlagAdmin)
