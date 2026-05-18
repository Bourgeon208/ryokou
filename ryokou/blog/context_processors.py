from .models import Conversation


def unread_messages_count(request):
    count = 0
    if request.user.is_authenticated:
        if request.user.is_staff:
            # Admin : messages non lus envoyés par les users
            from .models import Message
            count = Message.objects.filter(is_from_admin=False, read=False).count()
        else:
            # User : réponses admin non lues
            from .models import Message
            count = Message.objects.filter(
                is_from_admin=True,
                read=False,
                conversation__user=request.user
            ).count()
    return {'unread_messages_count': count}
