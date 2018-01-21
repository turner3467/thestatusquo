from django import template

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_site_root(context):
    # NB this returns a core.Page, not the implementation-specific model used
    # so object-comparison to self will return false as objects would differ
    return context['request'].site.root_page


def has_menu_children(page):
    return page.get_children().live().in_menu().exists()


@register.inclusion_tag('top_menu.html', takes_context=True)
def top_menu(context, parent, calling_page=None):
    menuitems = parent.get_children().filter(
        live=True,
        show_in_menus=True
    )
    for menuitem in menuitems:
        menuitem.show_dropdown = has_menu_children(menuitem)
    return {
        'calling_page': calling_page,
        'menuitems': menuitems,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


@register.filter(name='addcss')
def addcss(field, css):
    return field.as_widget(attrs={"class": css})
