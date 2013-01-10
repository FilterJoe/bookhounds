import re
import urllib2
import StringIO
from lxml import etree
from time import strftime, strptime
import books.models
#from django.shortcuts import render_to_response, render
#from django.http import HttpResponseRedirect, HttpResponse
#from views import get_amzn_URL, ask_for_URL_form

def get_amazon_url():
    # I wanted this routine to redirect to another web page to ask user to provide this URL
    # and then add basic validation.
    # but I couldn't figure out how to do it.
    # So all this was used for was testing.
    # u = 'http://www.amazon.com/Lucifers-Hammer-Larry-Niven/dp/0449208133'
    # u = 'http://www.amazon.com/Mote-Gods-Eye-Larry-Niven/dp/0671741926'
    # u = 'http://www.amazon.com/Ringworld-Larry-Niven/dp/0345333926'
    # u = 'http://www.amazon.com/Gripping-Hand-Larry-Niven/dp/0671795740'
    u = 'http://www.amazon.com/Enders-Game-Ender-Book-1/dp/0812550706'
    return u

def validated_amazon_URL_or_nil(u):
    '''
    input:  user supplied URL
    output: if valid, returns valid URL to Amazon
            else return empty string.
    notes:  checks a few things to make sure it's a valid amzn URL, including checking for the embedded 10 digit string.
            Will chop off all the irrelevant parts after the long number. Will add http:// if missing.
    '''
    if u[0:3] == 'www':
        print "adding http://"
        u1 = 'http://' + u
    elif u[0:7] == 'http://':
        u1 = u
    else:
        print "invalid url due to not starting with www or http://"
        return '','\nis not a valid Amazon URL. Unable to prefill data fields. You will have to do it manually.'
        # I think there is always a string in amazon book URLs that is 9 digits followed by an "X" or another digit
    embedded_book_id = re.search('[0-9,X]{10}', u1)
    if not embedded_book_id:
        print "invalid url due to not having embedded 10 digits"
        return '',"\nseems like a valid Amazon URL but there's something not quite right about it. Unable to prefill data fields. You will have to do it manually."
    else:
#        print "Start index:", embedded_book_id.start()
#        print "End index:", embedded_book_id.end()
#        print u1
        pass
    u2 = u1[:embedded_book_id.end()+1]
    return u2,''
def get_tree(u):
    '''
    input: u is a url such as 'http://www.xyz.com'
    output: lxml tree of the ElementTree class (NOT Element) or nil if there's a fatal error
    requirements:
        import urllib2
        import StringIO
        from lxml import etree (lxml must be installed)
    if you don't like this messy function, then get the requests package. See:
    https://gist.github.com/973705 and http://docs.python-requests.org/en/latest/
    '''
    tree = ''
    try:
        handler = urllib2.urlopen(urllib2.Request(u))
        broken_html = handler.read()
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO.StringIO(broken_html),parser)
    except ValueError:
        print "ERROR: unknown url type: %s" % u
    return tree

def get_amazon_book_data_string (tree,tag,attribute):
    '''
    inputs:
        tree (Elementtree class from lxml) that has parsed HTML from Amazon book web page.
        tag (HTML tag 'li' or 'meta[@content][@name="title"]'
        attribute (book attribute label on Amazon book web page such as
            'Publisher'
            'title'
    output: string (has data associated with the attribute on Amazon page held by tree)
    '''
    if tag == "li":
    # xPath = "string(//%s[contains(.,'%s')])" % (tag,attribute)
    # above barfed on Moneyball because there was a second 'Publisher:' on the page. Below corrects
    # Below corrects by picking out the last item no matter the number of items:
        xPath = "//%s[contains(.,'%s')]" % (tag,attribute)
        filtered_html = (etree.tostring(tree.xpath(xPath)[-1], method="text")).rstrip()
    elif tag[:4] == "meta":
        xPath = "//%s" % tag
        filtered_html = tree.xpath(xPath)[0].get("content") # a kludge - can I improve this?
    elif tag[:3] == "img":
        xPath = "//%s" % tag
        filtered_html = tree.xpath(xPath)[0].get("src")
    else:
        filtered_html = "error in get_amazon_data_string"
    return filtered_html

def prepopulate_with_error_message(g,amazon_book_url,message):
    g.update({
        'Amazon_book_data': amazon_book_url + message,
        })
    return g

def prepopulate_with_amazon_data(g,t,u):
    '''
    This is intertwined with the addview method of the bookadmin claass in admin.py, as it reads from and
    writes to DB (books.models.Publisher and books.models.Author). This is a little risky as the user does
    not see what the new publishers and authors look like. My goal was to make this incredibly easy
    to enter books.
    '''
    message = ''
    try:
        line1 = get_amazon_book_data_string(t, 'li', 'Publisher')
        line2 = get_amazon_book_data_string(t, 'li', 'ISBN-13')
        line3 = get_amazon_book_data_string(t, 'meta[@content][@name="title"]', 'title')
        line4 = get_amazon_book_data_string(t, 'img[@id="prodImage"]','prodImage')
        book_img = line4.split('_')[0] + 'jpg' # the unncessary junk between the '_' and .jpg is discarded
        amzn_data = (line1 + '\n' + line2 + '\n' + line3 + '\n' + book_img + '\n')
        section = line3.split(':')
        print section
        if section[0] == 'Amazon.com':
            section.pop(0)
        print section
        provisional_author_list = section[1].split(',')
        thing_after_author_list = section[2].split(',')
        pubsection = line1.split(':')
        almost_publishdate = (pubsection[1].split('('))[-1]
        publishdate= almost_publishdate.split(')')[0] # sometimes junk after ')' needs discarding
        temppublishername = pubsection[1].split('(')[0]
        if ';' in temppublishername:
            publishername = temppublishername.split(';')[0]
        else:
            publishername = temppublishername[:-1]
        p = books.models.Publisher.objects.filter(name=publishername[1:])
        if not p: # if publisher not in database, then add it
            new_pub = books.models.Publisher(name=publishername[1:])
            new_pub.save()
            # ':' is the delimiter between title and author, so below is my way of handling when ':' is
        # actually part of the title. I know the ISBN comes after author list, so I assign the thing right
        # before ISBN to author list, and all before goes to the title.
        if (thing_after_author_list[0])[1:].isdigit():
            author_list = provisional_author_list
            title = section[0]
        else:
            author_list = thing_after_author_list
            title = section[0] + ':' + provisional_author_list[0]
        author_ids = ''
        for i, val in enumerate(author_list):
            authorstring = author_list[i].split(' ')
            firstname = authorstring[1]
            lastname = authorstring[-1]
            middlename =''
            if len(authorstring)==4: # in the even there are more than 3 names, pick 2nd to last of them
                middlename = authorstring[-2]
            if len(middlename) == 1: # if no period after middle initial, want to put one there to avoid duplicate authors
                middlename += '.'
            a = books.models.Author.objects.filter(first_name = firstname,middle_name=middlename,last_name=lastname)
            if not a: # if author not in database, then add it
                new_author = books.models.Author(first_name=firstname,middle_name=middlename,last_name=lastname)
                new_author.save()

            auth = books.models.Author.objects.get(first_name = firstname,last_name=lastname)
            author_ids += str(auth.id) + ',' # contrib\admin\options.py to see why this was needed

        g.update({
            'title': title,
            'ISBN13': (line2.split(':')[1])[1:15], # note that ISBN is different for each edition of the book. ISBN a list?
            'Amazon_book_link': u,
            'image_URL': book_img,
            'Amazon_book_data': amzn_data,
            'publication_date': strftime('%Y-%m-%d', strptime(publishdate, '%B %d, %Y')),
            'publisher': books.models.Publisher.objects.get(name=publishername[1:]),
            'authors': author_ids,
            })
        return g, message
    except: # TO DO: must fix this catch all error clause to get more specific
        print "parsing choked in pre_populate_with_amazon_data"
        message = '\nis a valid Amazon URL but something about the page format was unusual.' \
                'Unable to parse the page and prefill the '\
                'data field. You will have to do it manually.'
        return '', message


