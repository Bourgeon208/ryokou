from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    title = models.CharField("Titre", max_length=200)
    slug = models.SlugField("Slug", unique=True, max_length=220)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name="Auteur")
    content = models.TextField("Contenu")
    video = models.FileField("Vidéo", upload_to='posts/videos/', blank=True, null=True)
    video_url = models.URLField("URL Vidéo (YouTube/Vimeo)", blank=True, null=True,
                                help_text="Entrez l'URL embed d'une vidéo YouTube ou Vimeo")
    created_at = models.DateTimeField("Créé le", default=timezone.now)
    updated_at = models.DateTimeField("Modifié le", auto_now=True)
    published = models.BooleanField("Publié", default=True)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post_detail', kwargs={'slug': self.slug})

    @property
    def comment_count(self):
        return self.comments.filter(approved=True).count()


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', verbose_name="Article")
    image = models.ImageField("Image", upload_to='posts/images/')
    caption = models.CharField("Légende", max_length=200, blank=True)
    order = models.PositiveIntegerField("Ordre", default=0)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
        ordering = ['order']

    def __str__(self):
        return f"Image #{self.order} — {self.post.title}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="Article")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name="Auteur")
    content = models.TextField("Commentaire")
    created_at = models.DateTimeField("Créé le", default=timezone.now)
    approved = models.BooleanField("Approuvé", default=True)

    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        ordering = ['created_at']

    def __str__(self):
        return f"Commentaire de {self.author.username} sur « {self.post.title} »"


class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations', verbose_name="Utilisateur")
    subject = models.CharField("Sujet", max_length=200)
    created_at = models.DateTimeField("Créée le", default=timezone.now)
    updated_at = models.DateTimeField("Dernier message", auto_now=True)

    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} — {self.subject}"

    @property
    def last_message(self):
        return self.messages.order_by('-created_at').first()

    @property
    def unread_for_admin(self):
        return self.messages.filter(read=False, is_from_admin=False).count()

    @property
    def unread_for_user(self):
        return self.messages.filter(read=False, is_from_admin=True).count()


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages', verbose_name="Conversation")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages', verbose_name="Auteur")
    content = models.TextField("Message")
    is_from_admin = models.BooleanField("De l'admin", default=False)
    created_at = models.DateTimeField("Envoyé le", default=timezone.now)
    read = models.BooleanField("Lu", default=False)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['created_at']

    def __str__(self):
        role = "Admin" if self.is_from_admin else self.author.username
        return f"{role} — {self.created_at:%d/%m/%Y %H:%M}"
