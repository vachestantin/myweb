
from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL) # 유저만이 글을 쓸 수 있음
    title = models.CharField(max_length=200, db_index=True)
    content = models.TextField(blank=False) # 제한이 없는 아주 큰 문자열
    photo = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True) # 처음 데이터가 들어갈때 생성 일시가 자동으로 들어가도록
    updated_at = models.DateTimeField(auto_now=True) # 저장 시점의 일시 정보를 입력

    tag = models.ManyToManyField('Tag', blank=True) # 'Tag' 모델 클래스의 이름을 문자열로 하는 이유는 장고가 나중에 처리하도록 하기 위해서. 문자열이 아닐 경우 Post 클래스보다 앞에 있어야 함.
    category = models.ForeignKey('Category', blank=False, null=False) # blank는 폼에서 사용하는 것 null은 db에서 사용하는 것

    is_model_field = False

    def __str__(self):
        return '{} - {} : {}'.format(self.pk, self.title, self.content)

    class Meta: # 디폴트 정렬 기준 설정 - 가장 최근글 우선
        ordering = ('-created_at', '-pk')


@receiver(post_delete, sender=Post)
def delete_attached_immage(sender, **kwargs):
    instance = kwargs.pop('instance')
    instance.photo.delete(save=False) # 이 명령이 사진 파일까지 지우게 된다. save가 True이면 삭제한 글이 자꾸 부활할 것이다.


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '({}) - {}.{} : {}'.format(self.pk, self.post.pk, self.post.title, self.content)


class Tag(models.Model):
     name = models.CharField(max_length=40)

     def __str__(self):
        return '({}) {}'.format(self.pk, self.name)


class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return '({}) {}'.format(self.pk, self.name)
