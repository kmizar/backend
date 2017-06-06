from django.contrib.sitemaps import Sitemap
from backend.models import Article, Flow, TagGroup
from django.core.urlresolvers import reverse

import datetime

#All published articles
class PostSitemap(Sitemap):
    changefreq = 'daily'
    priority   = 0.6

    def items(self):
        return Article.objects.filter(published_date__isnull=False).order_by('-published_date')

    def lastmod(self, article):
        return article.published_date

    def location(self, article):
        return '/post/{}'.format(str(article.id))


#All flows
#not used because its filter
class FlowSitemap(Sitemap):
    changefreq = 'daily'
    priority   = 0.8

    def items(self):
        return Flow.objects.all()

    def lastmod(self, flow):
        return datetime.datetime.now()

    def location(self, flow):
        return '/flows/{}'.format(flow.sys_name)


#All groups
#not used because its filter
class GroupSitemap(Sitemap):
    changefreq = 'daily'
    priority   = 0.8

    def items(self):
        return TagGroup.objects.all()

    def lastmod(self, group):
        return datetime.datetime.now()

    def location(self, group):
        return '/groups/{}'.format(group.sys_name)


#Home page
class HomeSitemap(Sitemap):
    priority   = 1
    changefreq = 'daily'
    pages      = ['home']

    def items(self):
        return self.pages

    def location(self, item):
        return reverse(item)
