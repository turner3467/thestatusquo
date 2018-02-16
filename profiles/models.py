from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailsearch import index
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    InlinePanel,
    PageChooserPanel
)
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailcore.models import Orderable

from modelcluster.fields import ParentalKey


class ProfileIndexPage(Page):
    intro = RichTextField(blank=True)
    subpage_types = [
        'profiles.PeopleProfilePage',
        'profiles.MediaProfilePage',
        'profiles.ThinkTankProfilePage',
    ]

    def get_context(self, request):
        context = super(ProfileIndexPage, self).get_context(request)

        context['media_profiles'] = \
            MediaProfilePage.objects.child_of(self).live()
        context['people_profiles'] = \
            PeopleProfilePage.objects.child_of(self).live()
        context['thinktank_profiles'] = \
            ThinkTankProfilePage.objects.child_of(self).live()
        return context


class ProfilePage(Page):
    publish_date = models.DateField('published date')
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('publish_date'),
        StreamFieldPanel('body'),
        ImageChooserPanel('feed_image'),
        InlinePanel('documents', label='Documents'),
        InlinePanel('links', label='Links'),
        InlinePanel('related_profiles', label='Related Profiles'),
    ]


class ProfilePageLink(Orderable):
    page = ParentalKey(ProfilePage, related_name='links')
    description = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('description'),
        FieldPanel('url'),
    ]


class ProfilePageDocuments(Orderable):
    page = ParentalKey(ProfilePage, related_name='documents')
    document = models.ForeignKey(
        'wagtaildocs.Document', on_delete=models.CASCADE, related_name='+'
    )

    panels = [
        DocumentChooserPanel('document'),
    ]


class RelatedProfile(Orderable):
    page = ParentalKey(ProfilePage, related_name='related_profiles')
    profile = models.ForeignKey(
        'profiles.ProfilePage', related_name='+'
    )

    panels = [
        PageChooserPanel('profile')
    ]


class PeopleProfilePage(ProfilePage):
    template = 'profiles/profile_page.html'


class MediaProfilePage(ProfilePage):
    template = 'profiles/profile_page.html'


class ThinkTankProfilePage(ProfilePage):
    template = 'profiles/profile_page.html'
