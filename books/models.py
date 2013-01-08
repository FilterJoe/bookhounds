from django.db import models

class Publisher(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=60, blank=True, null=True)
    state_province = models.CharField(max_length=30, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    def __unicode__(self):
        return self.name
    class meta:
        ordering = ('name',) # didn't do anything for generic view lists

class Author(models.Model):
    first_name = models.CharField(max_length=30, verbose_name="first")
    middle_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="m.")
    last_name = models.CharField(max_length=40, verbose_name="last")
    email = models.EmailField(blank=True, null=True)
    Amazon_author_link = models.URLField(blank=True, null=True)
    def __unicode__(self):
        return u'%s %s %s' % (self.first_name, self.middle_name, self.last_name)
    def author_books(self):
        alist = ''
        for a in self.books.all():
            alist += a.title + ', '
        return alist[:-2]
    author_books.short_description = 'books'
    class meta:
        ordering = ('last_name','first_name','middle_name') # didn't do anything for generic view lists
class Book(models.Model):
    title = models.CharField(max_length=100,blank=True, null=True)
    authors = models.ManyToManyField(Author, related_name='books')
    publisher = models.ForeignKey(Publisher, related_name='books')
    publication_date = models.DateField(blank=True, null=True, verbose_name="published")
    ISBN13 = models.CharField(max_length=14,unique=True)
    Amazon_book_link = models.URLField(blank=True, null=True)
    Amazon_book_data = models.TextField(max_length=400,blank=True,null=True)
    image_URL = models.URLField(blank=True, null=True)
    def __unicode__(self):
        return self.title
    def link_to_amazon(self):
        return '<a href="%s">%s</a>' % (self.Amazon_book_link, self.Amazon_book_link)
    link_to_amazon.short_description = 'Amazon link'
    link_to_amazon.allow_tags = True
    def admin_image(self):
        return '<a href="%s"><img src="%s" height="110" width="auto"></a>' % (self.Amazon_book_link,self.image_URL)
    admin_image.short_description = 'Amazon link'
    admin_image.allow_tags = True
    def linked_book_authors(self):
        alist=''
        for a in self.authors.all():
            alist += '<a href="/admin/books/author/%s">%s %s %s</a>, ' % (a.id, a.first_name,a.middle_name,a.last_name)
        return alist[:-2]
    linked_book_authors.allow_tags = True
    def book_authors(self):
        alist=''
        for a in self.authors.all():
            alist += '%s %s %s, ' % (a.first_name,a.middle_name,a.last_name)
        return alist[:-2]
    book_authors.allow_tags = True
    def b_lists(self):
    #        requires reverse many to many query, which took a little reading to figure out how to do
        BLlist=''
        for a in self.book_lists.all():
            if a:
                BLlist += '<a href="/admin/lists/booklist/%s">%s</a>, ' % (a.id, a.title)
                #gave me a ton of trouble because I forgot to start URL with a / so /admin/etc. was auto inserted
        return BLlist[:-2]
    b_lists.allow_tags = True
    b_lists.short_description = 'book lists'


class AuthorList(models.Model):
    title = models.CharField(max_length=128)
    authors = models.ManyToManyField(Author, through='AuthorInclusion', related_name='author_lists')
    short_description = models.TextField(max_length=256,blank=True,null=True)
    long_description = models.TextField(max_length=4096,blank=True,null=True)
    creator_name = models.CharField(max_length=32)
    def __unicode__(self):
        return self.title
class AuthorInclusion(models.Model):
    author = models.ForeignKey(Author)
    author_list = models.ForeignKey(AuthorList)
    rank = models.PositiveIntegerField()
    inclusion_reason = models.TextField(max_length=1024,blank=True,null=True, verbose_name='Why Include?')
    def __unicode__(self):
        return u'%s in %s' %(self.author,self.author_list.title)
    class Meta:
        ordering = ('rank',)

class BookList(models.Model):
    title = models.CharField(max_length=128)
    books = models.ManyToManyField(Book, through='BookInclusion', related_name='book_lists')
    short_description = models.TextField(max_length=256,blank=True,null=True)
    long_description = models.TextField(max_length=4096,blank=True,null=True)
    creator_name = models.CharField(max_length=32)
    def rank_ordered_books(self):
        return self.books.all().order_by('bookinclusion__rank') # took long time to figure this line out!!!
    def __unicode__(self):
        return self.title
        #    class Meta:
#        order_with_respect_to = ('books')
# this totall nuked access to db for booklists and bookinclusions. Wow. Did this crapify the database?
class BookInclusion(models.Model):
    book = models.ForeignKey(Book)
    book_list = models.ForeignKey(BookList)
    rank = models.PositiveIntegerField()
    inclusion_reason = models.TextField(max_length=1024,blank=True,null=True, verbose_name='Why Include?')
    def book_image(self):
        return '<a href="%s"><img src="%s" height="70" width="auto"></a>'\
               % (self.book.Amazon_book_link,self.book.image_URL)
    book_image.allow_tags = True
    def authors(self):
        return u'%s' %(self.book.linked_book_authors(),)
    authors.allow_tags = True
    def __unicode__(self):
        return u'%s by %s in %s' %(self.book,self.book.book_authors(),self.book_list.title)

    class Meta:
        ordering = ('rank',)
