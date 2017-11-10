from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
from django.db import models

# Create your models here.
from utils.fields.custom_imagefield import CustomImageField


class UserManager(DefaultUserManager):
    def create_user(self, email, password=None, name=None, nickname=None, **kwargs):
        user = self.model(email=self.normalize_email(email), is_active=True, **kwargs)
        user.name = name
        user.nickname = nickname
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password):
        user = self.create_user(email, password=password, nickname=nickname)
        user.email = email
        user.nickname = nickname
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user

    # 네이버로 가입하면 user_type을 N(Naver)으로 지정한다. 그외에 추가적인 정보를 커스텀 저장을 한다.
    def get_or_create_naver_user2(self, user_pk, extra_data):
        print(extra_data)
        user = User.objects.get(pk=user_pk)
        user.email = extra_data['email']
        user.name = extra_data['name']
        user.profile_image = extra_data['profile_image']
        user.user_type = "N"
        user.save()

        return user

    def get_or_create_naver_user(self, extra_data, password=None):
        user, user_created = self.get_or_create(
            email=extra_data['email'],
            profile_image=extra_data['profile_image'],
            user_type="N",
            name=extra_data['name'],
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def get_by_natural_key(self, email):
        return self.get(email=email)


class User(AbstractUser):
    USER_TYPE_DJANGO = 'D'
    USER_TYPE_FACEBOOK = 'F'
    USER_TYPE_NAVER = 'N'
    USER_TYPE_CHOICES = (
        (USER_TYPE_DJANGO, 'Django'),
        (USER_TYPE_FACEBOOK, 'Facebook'),
        (USER_TYPE_NAVER, 'Naver'),
    )

    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES, default='D')
    name = models.CharField(max_length=15, blank=True, null=True)  # 유저의 실제 이름
    username = models.CharField(max_length=30, unique=False)
    nickname = models.CharField(max_length=15, unique=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    post_code = models.CharField(max_length=10, blank=True, null=True)
    road_address = models.CharField(max_length=100, blank=True, null=True)
    detail_address = models.CharField(max_length=100, blank=True, null=True)

    profile_image = CustomImageField(
        upload_to='user_profile_img',
        blank=True,
        default_static_image='images/no_profile_image.jpg',
    )

    relations = models.ManyToManyField(
        'self',                 # 유저테이블끼리의 인스턴스간 관계를 가리키기 위해 'self'를 사용
        through='Relation',     # member_relation 테이블이 새로 생긴다.
        symmetrical=False,
    )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    # 위에서 커스터마이징한 UserManager를 사용할 수 있게 함.
    objects = UserManager()

    def __str__(self):
        return self.nickname or self.email

    def follow(self, user):
        # 매개변수로 전달된 user의 형(타입, = 클래스) 검사
        if not isinstance(user, User):
            raise ValueError('"user" argument must <User> class')

        # 해당 user를 follow하는 Relation을 생성한다.
        # 이미 follow 상태일 경우에는 아무일도 하지 않는다.

        # Relation 모델의 Manager를 사용하는 방법
        Relation.objects.get_or_create(from_user=self, to_user=user)

        # self로 주어진 User로부터 Relation의 from_user에 해당하는 RelatedManger를 사용
        # self.follow_realtions.get_or_create(to_user=user)

        # user로 주어진 User로부터 Relation의 to_user에 해당하는 RelatedManager를 사용
        # user.follow_relations.get_or_create(from_user=self)

    def unfollow(self, user):
        # 위의 반대 역할
        Relation.objects.filter(from_user=self, to_user=user).delete()

    def is_follow(self, user):
        # 이미 follow 상태면 unfollow하고 있는지 bool 여부를 반환
        # ModelManager.exists()를 사용
        # Relation을 검색하면 됨.
        return self.follow_relations.filter(to_user=user).exists()

    def is_follower(self, user):
        # 해당 유저가 나를 follow하고 있는지 bool여부를 반환
        return self.follower_relations.filter(from_user=user).exists()
        # return user.follow_relations.filter(to_user=self).exists()

    def follow_toggle(self, user):
        # 이미 follow상태면 unfollow, 아닐 경우 follow 상태로 만듬

        relation, relation_created = self.follow_relations.get_or_create(to_user=user)
        if not relation_created:
            relation.delete()
        else:
            return relation

class Relation(models.Model):
    # 같은 중요도로 참조할 수 있어야 한다.
    from_user = models.ForeignKey(
        User,
        related_name="follow_relations"
        # User가 두 군데서 쓰이기 때문에 역참조가 필요. 여기다가 역참조(relate_name)을 쓰면 User에서 접근이 가능하다.
    )
    to_user = models.ForeignKey(
        User,
        related_name="follower_relations"  # 나를 팔로우하고 있는 사람들
    )
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Relation from({}) to ({})'.format(
            self.from_user,
            self.to_user,
        )

    class Meta:
        unique_together = (
            ('from_user', 'to_user'),
        )