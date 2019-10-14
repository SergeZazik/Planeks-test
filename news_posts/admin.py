from django.contrib import admin
from .models import NewsPost


class NewsPostModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated', 'created']
    list_display_links = ['updated']
    list_editable = ['title']
    list_filter = ['updated', 'created']

    search_fields = ['title', 'content']

    prepopulated_fields = {'slug': ('title',)}

    class Meta:
        model = NewsPost


admin.site.register(NewsPost, NewsPostModelAdmin)

