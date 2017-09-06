import re
from django.conf import settings
from django.db import models
from post.models.others import Tag

__all__ = (
    'Post',
    'PostLike',
)


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=30)
    content = models.TextField()
    photo = models.ImageField(upload_to='post', blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)
    html_content = models.TextField(blank=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='PostLike',
        related_name='like_posts'
    )

    # 주소 관련 필드
    post_code = models.CharField(max_length=10, blank=True, null=True)
    road_address = models.CharField(max_length=100, blank=True, null=True)
    detail_address = models.CharField(max_length=100, blank=True, null=True)

    # 매물 등록 여부
    for_sale = models.BooleanField(default=False)
    for_sale_created_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    # 판매 여부
    is_sold = models.BooleanField(default=False)

    # 교환 횟수 카운트
    exchange_count = models.IntegerField(default=0)

    # 물품 카테고리 분류
    CATEGORY_TYPE_ELECTRONICS = 'e'
    CATEGORY_TYPE_FURNITURE = 'f'
    CATEGORY_TYPE_BEAUTY = 'be'
    CATEGORY_TYPE_CLOTHING = 'c'
    CATEGORY_TYPE_BOOK = 'bo'
    CATEGORY_TYPE_OTHERS = 'o'
    CATEGORY_TYPE_CHOICES = (
        (CATEGORY_TYPE_ELECTRONICS, '전자제품'),
        (CATEGORY_TYPE_FURNITURE, '가구'),
        (CATEGORY_TYPE_BEAUTY, '뷰티'),
        (CATEGORY_TYPE_CLOTHING, '옷'),
        (CATEGORY_TYPE_BOOK, '책'),
        (CATEGORY_TYPE_OTHERS, '기타'),
    )
    category = models.CharField(max_length=30, choices=CATEGORY_TYPE_CHOICES)

    # 거래방식 선택
    TRADING_TYPE_DIRECT = 'd'
    TRADING_TYPE_PARCEL = 'p'
    TRADING_TYPE_CHOICES = (
        (TRADING_TYPE_DIRECT, '직거래'),
        (TRADING_TYPE_PARCEL, '택배거래'),
    )
    trading_type = models.CharField(max_length=30, choices=TRADING_TYPE_CHOICES)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.make_html_content_and_add_tags()

    # 태그 생성
    def make_html_content_and_add_tags(self):
        p = re.compile(r'(#\w+)')
        tag_name_list = re.findall(p, self.content)
        ori_content = self.content
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name.replace('#', ''))
            change_tag = '<a href="">{}</a>'.format(tag_name)
            ori_content = re.sub(r'{}(?![<\w])'.format(tag_name), change_tag, ori_content, count=1)
            if not self.tags.filter(pk=tag.pk).exists():
                self.tags.add(tag)
        self.html_content = ori_content
        super().save(update_fields=['html_content'])

    # 매물 등록
    def make_for_sale(self):
        if not self.for_sale:
            self.for_sale = True
            self.save()
        else:
            self.for_sale = False
            self.save()


class PostLike(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='my_wishlist')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('post', 'user'),
        )


class Exchange(models.Model):
    post_item = models.ForeignKey(Post, related_name='post_item')
    comment_item = models.ForeignKey(Post, related_name='comment_item')

