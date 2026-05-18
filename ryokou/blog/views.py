from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Post, Comment, Conversation, Message
from .forms import RegisterForm, CommentForm, NewConversationForm, ReplyForm


def post_list(request):
    posts = Post.objects.filter(published=True).prefetch_related('images')
    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'blog/post_list.html', {'page_obj': page_obj})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    comments = post.comments.filter(approved=True).select_related('author')
    comment_form = CommentForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, "Connectez-vous pour commenter.")
            return redirect('login')
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Votre commentaire a été publié !")
            return redirect('post_detail', slug=slug)

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })


def register(request):
    if request.user.is_authenticated:
        return redirect('post_list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Bienvenue {user.username} !")
            return redirect('post_list')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def conversation_list(request):
    """Liste des conversations de l'utilisateur connecté."""
    if request.user.is_staff:
        # L'admin voit toutes les conversations
        conversations = Conversation.objects.all().prefetch_related('messages')
    else:
        conversations = Conversation.objects.filter(user=request.user).prefetch_related('messages')
    return render(request, 'blog/conversation_list.html', {'conversations': conversations})


@login_required
def new_conversation(request):
    """Démarre une nouvelle conversation avec l'admin."""
    if request.method == 'POST':
        form = NewConversationForm(request.POST)
        if form.is_valid():
            conversation = form.save(commit=False)
            conversation.user = request.user
            conversation.save()
            # Premier message
            Message.objects.create(
                conversation=conversation,
                author=request.user,
                content=form.cleaned_data['first_message'],
                is_from_admin=False,
            )
            messages.success(request, "Votre message a bien été envoyé !")
            return redirect('conversation_detail', pk=conversation.pk)
    else:
        form = NewConversationForm()
    return render(request, 'blog/new_conversation.html', {'form': form})


@login_required
def conversation_detail(request, pk):
    """Fil de conversation + formulaire de réponse."""
    if request.user.is_staff:
        conversation = get_object_or_404(Conversation, pk=pk)
    else:
        conversation = get_object_or_404(Conversation, pk=pk, user=request.user)

    # Marquer les messages comme lus
    if request.user.is_staff:
        conversation.messages.filter(is_from_admin=False, read=False).update(read=True)
    else:
        conversation.messages.filter(is_from_admin=True, read=False).update(read=True)

    reply_form = ReplyForm()

    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            msg = reply_form.save(commit=False)
            msg.conversation = conversation
            msg.author = request.user
            msg.is_from_admin = request.user.is_staff
            msg.save()
            # Touch updated_at
            from django.utils import timezone
            Conversation.objects.filter(pk=pk).update(updated_at=timezone.now())
            return redirect('conversation_detail', pk=pk)

    all_messages = conversation.messages.select_related('author')
    return render(request, 'blog/conversation_detail.html', {
        'conversation': conversation,
        'all_messages': all_messages,
        'reply_form': reply_form,
    })
