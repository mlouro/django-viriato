from django.contrib import admin
from newsletter.models import Subscriber,Group,Newsletter,Link,Submission

class SubscriberGroup(admin.ModelAdmin):
    list_display = ('name','email')
    list_filter = ('group',)
    search_fields = ('name',)

class NewsletterLink(admin.ModelAdmin):
    list_display = ('link','click_count',)
    list_filter = ('newsletter',)
    search_fields = ('newsletter','link',)
    
class NewsletterGroup(admin.ModelAdmin):
    list_display = ('title','view_count')
    list_filter = ('title','modified')
    search_fields = ('title',)
    
admin.site.register(Subscriber,SubscriberGroup)
admin.site.register(Group)
admin.site.register(Newsletter,NewsletterGroup)
admin.site.register(Link,NewsletterLink)
admin.site.register(Submission)