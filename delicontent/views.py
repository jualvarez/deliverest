# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404

from deliverest.decorators import render_to

from delicontent.models import Page


@render_to('delicontent/page.html')
def page(request, slug):
    page = get_object_or_404(Page, slug=slug)
    return {
        'page': page,
        'category_browse': True
    }
