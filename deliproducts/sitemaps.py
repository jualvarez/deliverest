from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from deliproducts.models import Category, Price


class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return Category.objects.filter(is_active=True)


class PriceSitemap(Sitemap):
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return Price.objects.filter(is_active=True, in_stock=True)

    def location(self, obj):
        return reverse('deliproducts.views.price', kwargs={'id': obj.id})


sitemaps = {
    'categorias': CategorySitemap,
    'productos': PriceSitemap
}
