from __future__ import absolute_import, unicode_literals

from django.shortcuts import render

from modelcluster.fields import ParentalKey
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, FieldRowPanel,
    InlinePanel, MultiFieldPanel,
    StreamFieldPanel
)
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField

from articles.models import ArticlePage
from profiles.models import ProfilePage


class HomePage(Page):
    subpage_types = [
        'profiles.ProfileIndexPage',
        'articles.ArticleIndexPage',
        'home.StandardPage',
        'home.ContactPage',
    ]

    def serve(self, request):
        articles = ArticlePage.objects.live().order_by('-publish_date')
        profiles = ProfilePage.objects.live().order_by('-last_published_at')

        return render(request, self.template, {
            'page': self,
            'articles': articles,
            'profiles': profiles,
        })


class StandardPage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]


class ContactFormField(AbstractFormField):
    page = ParentalKey('ContactPage', related_name='form_fields')


class ContactPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    exit_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('exit_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]
