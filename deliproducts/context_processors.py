from deliproducts.models import Category


def category_browse(request):
    return {'categories': Category.objects.filter(is_active=True, parent=None)}
