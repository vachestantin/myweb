from django import forms
from django.forms import ValidationError

from .models import Post


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'tag', 'category',)
        # exclude = ('title', 'category', ) # 사용하지 않을 필드만을 명시하는 기능
        # fields = '__all__' # 전체를 포함하고 싶은 경우

    def clean_title(self):
        title = self.cleaned_data.get('title', '', )
        if '바보' in title:
            raise ValidationError('바보스러운 기운이 난다.')
        return title.strip()

    def clean(self):
        super(PostEditForm, self).clean()
        title = self.cleaned_data.get('title', '')
        content = self.cleaned_data.get('content', '')

        if '안녕' in title:
            self.add_error('title', '안녕은 이제 그만 안녕')
        if '안녕' in content:
            self.add_error('content', '안녕은 이제 그만 안녕')
