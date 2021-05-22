from django.contrib import admin
from .models import VideoAllProxy, VideoPublishedProxy
# Register your models here.




class VideoAllAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'state','video_id', 'is_published']
    search_fields = [ 'title' ]
    list_filter = ['active', 'state']
    readonly_fields = ['id', 'is_published', 'publish_timestamp']
    class Meta:
        model = VideoAllProxy


class VideoPublishedProxyAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_id', 'active']
    search_fields = [ 'title' ]
    class Meta:
        model = VideoPublishedProxy

    def get_queryset(self, request):
        return VideoPublishedProxy.objects.filter(active=True)


admin.site.register(VideoAllProxy, VideoAllAdmin)
admin.site.register(VideoPublishedProxy, VideoPublishedProxyAdmin)