from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone as tz
from django.shortcuts import redirect
from django.contrib import messages as flash
from .models import Post, PostImage, Comment, Conversation, Message


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 3
    fields = ['image', 'caption', 'order']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'published', 'comment_count_display']
    list_filter = ['published', 'created_at', 'author']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['published']
    inlines = [PostImageInline]
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Contenu', {'fields': ('title', 'slug', 'author', 'content', 'published')}),
        ('Médias vidéo', {'fields': ('video', 'video_url'), 'classes': ('collapse',)}),
        ('Dates', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    @admin.display(description='Commentaires')
    def comment_count_display(self, obj):
        return format_html('<span style="font-weight:bold">{}</span>', obj.comment_count)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_at', 'approved', 'short_content']
    list_filter = ['approved', 'created_at']
    search_fields = ['content', 'author__username', 'post__title']
    list_editable = ['approved']
    actions = ['approve_comments', 'reject_comments']

    @admin.display(description='Aperçu')
    def short_content(self, obj):
        return obj.content[:80] + '...' if len(obj.content) > 80 else obj.content

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
    approve_comments.short_description = "Approuver les commentaires sélectionnés"

    def reject_comments(self, request, queryset):
        queryset.update(approved=False)
    reject_comments.short_description = "Rejeter les commentaires sélectionnés"


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['sujet_avec_badge', 'user', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['subject', 'user__username']
    # Pas de fields/readonly_fields : on gère tout dans le template custom

    @admin.display(description='Sujet')
    def sujet_avec_badge(self, obj):
        count = obj.unread_for_admin
        badge = ''
        if count:
            badge = (
                f'<span style="background:#c8432a;color:white;padding:1px 7px;'
                f'border-radius:10px;font-size:11px;margin-left:8px">'
                f'{count} nouveau{"x" if count > 1 else ""}</span>'
            )
        return format_html('<span>{}</span>{}', obj.subject, badge)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)

        # Traitement de la réponse
        if request.method == 'POST' and '_send_reply' in request.POST:
            content = request.POST.get('_reply_content', '').strip()
            if content and obj:
                Message.objects.create(
                    conversation=obj,
                    author=request.user,
                    content=content,
                    is_from_admin=True,
                    read=False,
                )
                Conversation.objects.filter(pk=obj.pk).update(updated_at=tz.now())
                flash.success(request, "Réponse envoyée !")
            return redirect('.')

        # Marquer les messages user comme lus
        if obj:
            obj.messages.filter(is_from_admin=False, read=False).update(read=True)

        extra_context = extra_context or {}
        extra_context['messages_list'] = obj.messages.all() if obj else []
        extra_context['original'] = obj

        return super().change_view(request, object_id, form_url, extra_context)

    def has_add_permission(self, request):
        return False
