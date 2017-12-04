from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    InlinePanel
)
from wagtail.wagtailsearch import index
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailcore.models import Orderable

from modelcluster.fields import ParentalKey


class ArticleIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]


class ArticlePage(Page):
    publish_date = models.DateField('published date')
    intro = models.CharField(max_length=250)
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('publish_date'),
        FieldPanel('intro'),
        StreamFieldPanel('body'),
        InlinePanel('links', label='Links')
    ]


class ArticlePageLink(Orderable):
    page = ParentalKey(ArticlePage, related_name='links')
    description = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('description'),
        FieldPanel('url'),
    ]
