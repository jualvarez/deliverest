from delicontent.models import Page


def nav_pages(request):
    return {'nav_pages': Page.objects.filter(show_in_nav=True)}
