
from django.contrib import admin
from .models import *


class CommentInlineAdmin(admin.StackedInline):
    model = Comment
    extra = 1 # 페이지에 표시할 댓글 입력 칸 수

class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title','created_at', 'category',)
    list_display_links = ('pk', 'title',)
    ordering = ('-id',)
    inlines = [CommentInlineAdmin] # posts를 수정할때 댓글도 수정할 수 있다
    search_fields = ('title', 'content',) # 이상하게도 태그랑 카테고리는 검색할 수 없다
    list_filter = ('category', 'tag', 'created_at',) # 우측에 필터로 정리 (가장 마음에 드는 기능)
    date_hierarchy = 'created_at' # 날짜를 다루기 때문에 pytz를 설치해야 한다. (에러가 뜰 경우: pip install pytz)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Category)
