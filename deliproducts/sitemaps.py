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
        return Price.objects.all()

    def location(self, obj):
        return reverse('deliproducts.views.price', kwargs={'slug_id': obj.slug_id})


sitemaps = {
    'categorias': CategorySitemap,
    'productos': PriceSitemap
}
