from django.db import models
from django.shortcuts import render

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    InlinePanel,
    PageChooserPanel,
)
from wagtail.wagtailsearch import index
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailcore.models import Orderable
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey


class ArticleIndexPage(Page):
    intro = RichTextField(blank=True)
    subpage_types = ['articles.ArticlePage']

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def serve(self, request):
        # Get blogs
        articles = ArticlePage.objects.child_of(self).live()

        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            articles = articles.filter(tags__name=tag)

        return render(request, self.template, {
            'page': self,
            'articles': articles,
            'tag': tag,
        })


class ArticlePageTag(TaggedItemBase):
    content_object = ParentalKey(
        'articles.ArticlePage',
        related_name='article_tags'
    )


class ArticlePage(Page):
    publish_date = models.DateField('published date')
    intro = models.CharField(max_length=250)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('embed', EmbedBlock()),
    ])

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    tags = ClusterTaggableManager(
        through=ArticlePageTag,
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('publish_date'),
        FieldPanel('intro'),
        StreamFieldPanel('body'),
        ImageChooserPanel('feed_image'),
        InlinePanel('article_profile_link', label='Profiles'),
        InlinePanel('documents', label='Documents'),
        InlinePanel('links', label='Links'),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('tags')
    ]


class ArticlePageLink(Orderable):
    page = ParentalKey(ArticlePage, related_name='links')
    description = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('description'),
        FieldPanel('url'),
    ]


class ArticlePageDocuments(Orderable):
    page = ParentalKey(ArticlePage, related_name='documents')
    document = models.ForeignKey(
        'wagtaildocs.Document', on_delete=models.CASCADE, related_name='+'
    )

    panels = [
        DocumentChooserPanel('document'),
    ]


class ArticlePageProfiles(Orderable):
    page = ParentalKey(
        ArticlePage,
        related_name='article_profile_link'
    )
    profile = models.ForeignKey(
        'profiles.ProfilePage',
        related_name='profile_article_link'
    )

    panels = [
        PageChooserPanel('profile')
    ]
