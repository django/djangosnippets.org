from django.contrib import admin
from cab.models import Language, Snippet

class LanguageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}

admin.site.register(Language, LanguageAdmin)
admin.site.register(Snippet)
