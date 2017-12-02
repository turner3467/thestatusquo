from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel


class ProfileIndexPage(Page):
    intro = RichTextField(blank=True)


class ProfilePage(Page):
    publish_date = models.DateField('published date')
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('publish_date'),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
    ]
