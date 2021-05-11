from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['group', 'text', 'image']
        labels = {
            'group': 'Группа',
            'text': 'Текст поста',
            'image': 'Изображение'
        }
        help_texts = {
            'group': 'Выберите группу, в которой публикуете пост',
            'text': 'Расскажите что-нибудь интересное',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
