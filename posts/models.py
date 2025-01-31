from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model

class Category(models.Model):
    title = models.CharField(_("عنوان دسته بندی"), max_length=50)
    description = models.TextField(_("توضیحات"), blank=True)  # حذف null=True
    slug = models.SlugField(_("عنوان لاتین"))
    created_time = models.DateTimeField(
        _("زمان ایجاد"), auto_now=False, auto_now_add=True
    )

    class Meta:
        db_table = "Category"
        managed = True
        verbose_name = _("دسته بندی")
        verbose_name_plural = _("دسته بندی ها")

    def __str__(self):
        return self.title


class Tag(models.Model):
    postFore = models.ForeignKey(
        "Post", related_name="postTags", on_delete=models.CASCADE, null=True
    )
    title = models.CharField(_("عنوان تگ"), max_length=50)
    description = models.TextField(_("توضیحات"), blank=True)  # حذف null=True
    slug = models.SlugField(_("عنوان لاتین"))
    created_time = models.DateTimeField(
        _("زمان ایجاد"), auto_now=False, auto_now_add=True
    )

    class Meta:
        verbose_name = _("تگ")
        verbose_name_plural = _("تگ ها")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Tag_detail", kwargs={"pk": self.pk})


class Post(models.Model):
    title = models.CharField(_("عنوان"), max_length=50)
    content = models.TextField(_("توضیحات"))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("نویسنده"), on_delete=models.CASCADE
    )
    created_time = models.DateTimeField(_("زمان ایجاد"), auto_now_add=True)
    published_time = models.DateTimeField(_("زمان تغییرات"), auto_now=True)
    image = models.ImageField(_("تصویر مقاله"), upload_to="Posts/%Y/%m/%d")
    categories = models.ForeignKey(
        Category,
        verbose_name=_("دسته بندی"),
        related_name="posts",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    tags = models.ManyToManyField(Tag, verbose_name=_("تگ ها"), default="تگ اول")
    is_approved = models.BooleanField(_("تایید شده"), default=False)

    class Meta:
        verbose_name = _("مقاله")
        verbose_name_plural = _("مقالات")

    def __str__(self):
        return self.title or "بدون عنوان"

    def get_absolute_url(self):
        return reverse("Post_detail", kwargs={"pk": self.pk})



class Comment(models.Model):
    blog = models.ForeignKey(
        "Post",
        verbose_name=_("مقاله"),
        related_name=("comments"),
        on_delete=models.CASCADE,
    )

    name = models.CharField(_("نام کاربر"), max_length=50)
    email = models.EmailField(_("ایمیل کاربر"), max_length=254)
    message = models.TextField(_("پیام"))
    created_at = models.DateTimeField(_("زمان نوشتن نظر"), auto_now_add=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("کاربر"), on_delete=models.CASCADE
    )

    class Meta:
        db_table = "Comment"
        managed = True
        verbose_name = _("نظر")
        verbose_name_plural = _("نظرات")

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=50)
    message = models.TextField(_("پیغام شما"))
    created_time = models.DateTimeField(
        _("زمان ایجاد پیغام"), auto_now=False, auto_now_add=True
    )
    is_answered = models.BooleanField(_("وضعیت پاسخ"), default=False)

    class Meta:
        verbose_name = _("پیغام")
        verbose_name_plural = _("پیغام ها")

    def __str__(self):
        return self.name


class Answer(models.Model):
    contact = models.OneToOneField(
        Contact,
        verbose_name=_("سوالات"),
        on_delete=models.CASCADE,
        related_name="conracts",
    )

    respondent_admin = models.CharField(_("ادمین پاسخ دهنده"), max_length=50)
    response = models.TextField(_("متن جواب"))
    answer_time = models.DateTimeField(_("زمان پاسخ"), auto_now_add=True)

    class Meta:
        verbose_name = _("جواب")
        verbose_name_plural = _("جواب ها")

    def __str__(self):
        return self.respondent_admin

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"