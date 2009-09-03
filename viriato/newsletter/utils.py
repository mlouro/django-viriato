
#----------------------------------------------------------------------
def store_link(html, newsletter_instance):
    """Store links ate the database"""
    import httplib2, urllib2, lxml
    from lxml.html import iterlinks
    temp_links = iterlinks(html)
    
    import hashlib
    Link.objects.filter(newsletter=newsletter_instance).delete()
    
    import random
    rand = str(random.random())
    salt = hashlib.sha1(rand).hexdigest()[:5]
    
    for ele in temp_links:
        link = Link()
        link.link = ele[2]
        link.newsletter = newsletter_instance
        link.created_hash = hashlib.sha1(salt+ele[2]).hexdigest()
        link.click_count = 0
        link.save()

#----------------------------------------------------------------------
def get_newsletter_url(formset):
    """Get the Newsletter Url and store the html"""
    
    instance = formset.save(commit=False)
    import httplib2, urllib2, lxml
    from lxml.html import fromstring, make_links_absolute
    url = instance.url
    content = urllib2.urlopen(url,"text/html").read()
    doc = fromstring(content)
    doc.make_links_absolute(url)
    html = lxml.html.tostring(doc,pretty_print=True, method="html")
    instance.content = html
    instance.save()
    
    """save links"""
    store_link(html, instance)