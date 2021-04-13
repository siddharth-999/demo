from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .helpers import UserManager

RELATION_CHOICE = (
    (0, "Sibling"),
    (1, "Parent"),
    (2, "Children"),
    (3, "Grand Parent"),
    (4, "Cousin")
)


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True,
                                      verbose_name=_("Created At"),
                                      auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, db_index=True,
                                       verbose_name=_("Modified At"))

    class Meta:
        abstract = True


class Family(BaseModel):
    name = models.CharField(max_length=254,
                            verbose_name=_("Family Name"),
                            null=True, blank=True)

    def __str__(self):
        return str(self.name)


class User(AbstractUser, BaseModel):
    first_name = models.CharField(max_length=254,
                                  verbose_name=_("First Name"),
                                  null=True, blank=True)
    last_name = models.CharField(max_length=254,
                                 verbose_name=_("Last Name"),
                                 null=True, blank=True)
    is_delete = models.BooleanField(verbose_name=_("Is Delete"),
                                    default=False)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.BigIntegerField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    family = models.ForeignKey(Family, on_delete=models.SET_NULL,
                               null=True, blank=True)
    USERNAME_FIELD = settings.AUTH_USERNAME_FIELD
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return str(self.username)


class FamilyRelation(BaseModel):
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL,
                                 null=True, blank=True)
    relation = models.IntegerField(null=True, blank=True,
                                   choices=RELATION_CHOICE)
    relative = models.ForeignKey(User, on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 related_name="user_relative")
