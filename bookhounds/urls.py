from django.conf.urls import patterns, include, url
from books.views import home_page, ask_for_URL_form, get_amzn_URL, mybookslider_page
from books.views import PublisherList, PublisherDetail, AuthorList, AuthorDetail
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BookHounds.views.home', name='home'),
    # url(r'^BookHounds/', include('BookHounds.foo.urls')),
    url(r'^$',home_page),
    url(r'^admin/books/book/betteradd/', ask_for_URL_form), # from list
    url(r'^admin/books/book/[0-9]+/betteradd/', ask_for_URL_form), # from change form
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^book-search-form/', ask_for_URL_form),
    url(r'^book-search/', get_amzn_URL),
    url(r'^my-books/', mybookslider_page),
    url(r'^publishers/$',PublisherList.as_view()),
    url(r'^publisher/(?P<pk>\d+)/$',PublisherDetail.as_view()),
    url(r'^authors/$',AuthorList.as_view()),
    url(r'^author/(?P<pk>\d+)/$',AuthorDetail.as_view()),
)