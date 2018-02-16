# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-16 20:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('profiles', '0001_initial'),
        ('wagtaildocs', '0007_merge'),
        ('articles', '0001_initial'),
        ('wagtailimages', '0019_delete_filter'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepageprofiles',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_article_link', to='profiles.ProfilePage'),
        ),
        migrations.AddField(
            model_name='articlepagelink',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='articles.ArticlePage'),
        ),
        migrations.AddField(
            model_name='articlepagedocuments',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtaildocs.Document'),
        ),
        migrations.AddField(
            model_name='articlepagedocuments',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='articles.ArticlePage'),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='feed_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='articles.ArticlePageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
