from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext # to get my css file to be seen
from django.views.generic import ListView, DetailView
from books.models import Publisher, Author, Book, BookList

def home_page(request):
    BookList_list = BookList.objects.order_by('title')
    return render_to_response('home.html', locals(), context_instance=RequestContext(request))

def mybookslider_page(request):
    Books = Book.objects.order_by('title')
    return render_to_response('mybookslider.html', locals(), context_instance=RequestContext(request))

def ask_for_URL_form(request):
    return render_to_response('amazon_URL_request.html', context_instance=RequestContext(request))

def get_amzn_URL(request):
    url = str(request.GET['url'])
    if url == "": # Django tutorial example didn't work right so I corrected with this
        message = 'You submitted an empty form.'
    else:
        message = 'you submitted: %r' % request.GET['url']
    print message
    return HttpResponseRedirect('') # I don't understand why this is working . . .
#    return HttpResponse(request.GET['url'])



'''
Below are experiments with generic views. They took a bit of learning, make the code less clear, and offer
little flexibility. For example, I don't think I can embed them on a part of the page - they take over an
entire page. What's the point?
'''

class PublisherList(ListView): # note that default auto generated template name is books/publisher_list.html
    model = Publisher
    queryset = Publisher.objects.order_by('name') # only needed because I wanted it sorted
class PublisherDetail(DetailView):
    model = Publisher
    context_object_name = 'publisher_entry'
    queryset = Publisher.objects.all()

class AuthorList(ListView): # note that default auto generated template name is books/publisher_list.html
    model = Author
    queryset = Author.objects.order_by('last_name') # only needed because I wanted it sorted

class AuthorDetail(DetailView):
    model = Author
    context_object_name = 'author_entry'
    queryset = Author.objects.all()
