# Generated by Django 5.1.5 on 2025-02-10 13:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان دسته بندی')),
                ('description', models.TextField(blank=True, verbose_name='توضیحات')),
                ('slug', models.SlugField(verbose_name='عنوان لاتین')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
                'db_table': 'Category',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('message', models.TextField(verbose_name='پیغام شما')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد پیغام')),
                ('is_answered', models.BooleanField(default=False, verbose_name='وضعیت پاسخ')),
            ],
            options={
                'verbose_name': 'پیغام',
                'verbose_name_plural': 'پیغام ها',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respondent_admin', models.CharField(max_length=50, verbose_name='ادمین پاسخ دهنده')),
                ('response', models.TextField(verbose_name='متن جواب')),
                ('answer_time', models.DateTimeField(auto_now_add=True, verbose_name='زمان پاسخ')),
                ('contact', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='conracts', to='posts.contact', verbose_name='سوالات')),
            ],
            options={
                'verbose_name': 'جواب',
                'verbose_name_plural': 'جواب ها',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('content', models.TextField(verbose_name='توضیحات')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('published_time', models.DateTimeField(auto_now=True, verbose_name='زمان تغییرات')),
                ('image', models.ImageField(upload_to='Posts/%Y/%m/%d', verbose_name='تصویر مقاله')),
                ('is_approved', models.BooleanField(default=False, verbose_name='تایید شده')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='نویسنده')),
                ('categories', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='posts.category', verbose_name='دسته بندی')),
            ],
            options={
                'verbose_name': 'مقاله',
                'verbose_name_plural': 'مقالات',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='نام کاربر')),
                ('email', models.EmailField(max_length=254, verbose_name='ایمیل کاربر')),
                ('message', models.TextField(verbose_name='پیام')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='زمان نوشتن نظر')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.post', verbose_name='مقاله')),
            ],
            options={
                'verbose_name': 'نظر',
                'verbose_name_plural': 'نظرات',
                'db_table': 'Comment',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان تگ')),
                ('description', models.TextField(blank=True, verbose_name='توضیحات')),
                ('slug', models.SlugField(verbose_name='عنوان لاتین')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('postFore', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='postTags', to='posts.post')),
            ],
            options={
                'verbose_name': 'تگ',
                'verbose_name_plural': 'تگ ها',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(default='تگ اول', to='posts.tag', verbose_name='تگ ها'),
        ),
    ]
