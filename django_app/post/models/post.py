from django.db import models

from config import settings


__all__ = (
    'Post',
    'PostLike',
)


class Post(models.Model):
    author = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    content = models.TextField()
    photo = models.ImageField(upload_to='post', blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    hash_tag = models.CharField(max_length=30)
    my_comment = models.CharField(max_length=30)
    ##########
    like_users = models.ManyToManyField(
        settings.base.AUTH_USER_MODEL,
        through='PostLike',
        related_name='like_posts'
    )
    # 판매 여부
    is_sold = models.BooleanField()
    # 교환 횟수 카운트
    exchange_count = models.IntegerField()
    # 판매자 위치
    location = models.CharField(max_length=50)

    # 물품 카테고리 분류
    CATEGORY_TYPE_ELECTRONICS = 'e'
    CATEGORY_TYPE_FURNITURE = 'f'
    CATEGORY_TYPE_BEAUTY = 'be'
    CATEGORY_TYPE_CLOTHING = 'c'
    CATEGORY_TYPE_BOOK = 'bo'
    CATEGORY_TYPE_CHOICES = (
        (CATEGORY_TYPE_ELECTRONICS, 'Electronics'),
        (CATEGORY_TYPE_FURNITURE, 'Furniture'),
        (CATEGORY_TYPE_BEAUTY, 'Beauty'),
        (CATEGORY_TYPE_CLOTHING, 'Clothing'),
        (CATEGORY_TYPE_BOOK, 'Book'),
    )
    category = models.CharField(max_length=30, choices=CATEGORY_TYPE_CHOICES)

    # 거래방식 선택
    TRADING_TYPE_DIRECT = 'd'
    TRADING_TYPE_PARCEL = 'p'
    TRADING_TYPE_CHOICES = (
        (TRADING_TYPE_DIRECT, 'Direct'),
        (TRADING_TYPE_PARCEL, 'Parcel'),
    )
    trading_type = models.CharField(max_length=30, choices=TRADING_TYPE_CHOICES)


class PostLike(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(settings.base.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('post', 'user'),
        )