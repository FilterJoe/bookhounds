from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea, ModelForm, CharField
from books.models import Publisher, Author, Book
from books.models import AuthorList, AuthorInclusion, BookList, BookInclusion
from button_admin import ButtonAdmin
import scrape_amazon_utils # must do it this way in order to avoid dependency issues


class BookInline(admin.StackedInline):
    model = Book
    fields = (('admin_image', 'ISBN13', 'publisher','publication_date'),
              ('title', 'authors',))
    readonly_fields = ('authors','admin_image','title', 'ISBN13','publisher','publication_date')
    extra = 0
class AuthorBookInLine(admin.StackedInline):
    # lists books in author change_view. Note that readonly_fields not permitted for manytomany Inlines
    model = Book.authors.through
    extra = 0
class AuthorListInLine(admin.StackedInline):
    model = AuthorList.authors.through
    extra = 0
class PublisherAdmin(admin.ModelAdmin):
    fields = (('name','website','address'),
              ('city','state_province','country'))
    save_on_top = True # puts the save button on top
    search_fields = ('name',)
    ordering = ('name',)
    inlines = [
        BookInline,
        ]
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name','middle_name','author_books')
    search_fields = ('first_name','last_name','books__title')
    ordering = ('last_name','first_name','middle_name')
    save_on_top = True # puts the save button on top
    inlines = [
        AuthorBookInLine,
        AuthorListInLine,
        ]
class BookAdmin(ButtonAdmin):
    # ButtonAdmin is a fancier admin.ModelAdmin that allows adding buttons in addition to history
    fields = ('Amazon_book_link',
              'Amazon_book_data',
              ('title', 'ISBN13'),
              'image_URL',
              ('publisher','publication_date'),
              'authors',)
    formfield_overrides = {

        # Below first line is commmented out due to following bug:
        # When in, Django would enforce the maximum field length of 14 (from ISBN) onto 'title' field
        # on the change form (but not at DB level). So I couldn't modify title. This wasn't always true
        # so there is probably a subtle bug that is caused by a recent code addition that somehow interacts
        # with max_length and formfield_overrides.

        #        models.CharField: {'widget': TextInput(attrs={'size':'30'})},
        models.URLField: {'widget': TextInput(attrs={'size':'81'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':78})},
        }
    list_display = ('title','linked_book_authors','b_lists','ISBN13','publication_date','admin_image')
    #    list_filter = ('publication_date',)
    #    date_hierarchy = 'publication_date'
    ordering = ('title','publisher','-publication_date')
    list_per_page = 10
    # raw_id_fields = ('publisher',)
    filter_horizontal = ('authors',)
    save_on_top = True # puts the save button on top
    search_fields = ['title','authors__first_name', 'authors__middle_name', 'authors__last_name']
    # notice how many to many "authors" field is accessed via double__underscore notation
    def add_view(self, request, form_url='', extra_context=None):
        '''
        Overrides admin's add_view in order to prepopulate all input fields with data extracted
        from Amazon web page u. If publisher (or author) not in database, then new publisher (or author)
        is added. I would like to add image field to context but can't because not in DB yet.
        '''
        amazon_book_url = request.GET.get('amzn_url','')
        g = request.GET.copy()
        message = ''
        u,message = scrape_amazon_utils.validated_amazon_URL_or_nil(amazon_book_url)
        if u:
            t = scrape_amazon_utils.get_tree(u) # uses lxml to parse u into a tree structure
            if t:
                newget,parse_message = scrape_amazon_utils.prepopulate_with_amazon_data(g,t,u)
                if newget:
                    print "newget is: ", newget
                    request.GET = newget
                else:
                    message = parse_message
                    print "newget is nil"
            else:
                message = '\nis a valid but unusual Amazon URL. Unable to prefill ' \
                          'data field. You will have to do it manually.'
        if message:
            request.GET = scrape_amazon_utils.prepopulate_with_error_message(g,amazon_book_url,message)
        return super(BookAdmin, self).add_view(request, form_url, extra_context=extra_context)



    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context =\
        {"book_img_url" : Book.objects.get(id=object_id).image_URL,
         "book_title" : Book.objects.get(id=object_id).title,
         "lists_this_book_is_on" : Book.objects.get(id=object_id).book_lists.all().order_by('title'),
         }
        return super(BookAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)



    def betteradd(self, request, obj=None):
        '''
        This never executes. The button code just grabs this name and appends it to admin/books/book, to get:
        admin/books/book/betteradd/ and it's up to me to have urls.py map this to appropriate view.
        '''
        print "in better_add method" # this never executes. So what is the point of this method?
        if obj is not None: obj.bar()
        return None # Redirect or Response or None
        # Confusion . . . why is HttpResponseRedirect('Amazon_URL_request.html') not needed?

    betteradd.short_description='Much Faster Way to Add Book'
    list_buttons = [ betteradd ]
    change_buttons = [ betteradd ]



class AuthorListInLine(admin.StackedInline):
    model = AuthorList.authors.through
    raw_id_fields = ('author',)
    extra = 1

class AuthorListAdmin(admin.ModelAdmin):
    save_on_top = True # puts the save button on top
    list_display = ('title','creator_name','short_description')
    #    search_fields = ('title')
    ordering = ('title','creator_name')
    inlines = [
        AuthorListInLine,
        ]

class BookListInLine(admin.TabularInline):
    model = BookList.books.through
    fields = (('book_image','book', 'rank',),
              ('inclusion_reason',))
    readonly_fields = ('book_image',) # this was required to avoid getting Django error message
    raw_id_fields = ('book',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':83})},
        }
    extra = 1

class BookListAdmin(admin.ModelAdmin):
    save_on_top = True # puts the save button on top
    list_display = ('title','creator_name','short_description')
    #    search_fields = ('title')
    ordering = ('title',)
    inlines = [
        BookListInLine,
        ]
    formfield_overrides = {
        #        models.CharField: {'widget': TextInput(attrs={'size':'30'})},
        #        models.URLField: {'widget': TextInput(attrs={'size':'81'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':83})},
        }
class BookInclusionAdmin(admin.ModelAdmin):
    save_on_top = True # puts the save button on top
    list_display = ('book','authors','book_list','rank')
    list_display_links = ('book','book_list',)



admin.site.register(AuthorList, AuthorListAdmin)
admin.site.register(AuthorInclusion)
admin.site.register(BookList, BookListAdmin)
admin.site.register(BookInclusion,BookInclusionAdmin)

admin.site.register(Publisher,PublisherAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book,BookAdmin)

