# Generated by Django 2.0.7 on 2018-07-27 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='動画URL')),
                ('title', models.TextField(verbose_name='動画タイトル')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='生成日時')),
                ('count', models.IntegerField(default=0, verbose_name='アクセス回数')),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('short_id', models.SlugField(max_length=6, primary_key=True, serialize=False)),
                ('url', models.URLField(verbose_name='プレイリストURL')),
                ('title', models.TextField(verbose_name='プレイリストタイトル')),
                ('count', models.IntegerField(default=0, verbose_name='アクセス回数')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='生成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='playlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movies', to='ml2lm.Playlist', verbose_name='プレイリスト'),
        ),
    ]
