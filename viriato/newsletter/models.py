# -*- coding: utf-8 -*-
from django.db import models
import datetime
from lxml.html import parse, iterlinks, make_links_absolute,tostring,fromstring

########################################################################
class Group(models.Model):
    """Groups data"""
    name = models.CharField(blank = False, unique=True, max_length=60)
    created = models.DateTimeField(blank=False, auto_now_add=True)
    modified = models.DateTimeField(blank=False, auto_now=True)
    #----------------------------------------------------------------------
    def __unicode__(self):
        """return the group name"""
        return self.name
    #----------------------------------------------------------------------
    @models.permalink
    def get_absolute_url(self):
        """return the absolute url"""
        return ('group_update', [str(self.id)])
    #----------------------------------------------------------------------
    @models.permalink
    def get_delete_url(self):
        """Return the delete url"""
        return('group_delete',[str(self.id)])
    #----------------------------------------------------------------------
    @models.permalink
    def get_subscriber_by_group_url(self):
        """Return the filter url"""
        return ('subscriber_by_group', [str(self.id)])

########################################################################
class Subscriber(models.Model):
    """Subscribers data"""
    name = models.CharField(max_length=60)
    group = models.ManyToManyField(Group)
    email = models.EmailField(unique=True)
    created = models.DateTimeField(blank=False, auto_now_add=True)
    modified = models.DateTimeField(blank=False, auto_now=True)
    subscribed = models.BooleanField(default=True)
    #----------------------------------------------------------------------
    def __unicode__(self):
        """return the subscriber name"""
        return self.name
    #----------------------------------------------------------------------
    @models.permalink
    def get_absolute_url(self):
        """Return the absolute url"""
        return ('subscriber_update', [str(self.id)])
    #----------------------------------------------------------------------
    @models.permalink
    def get_edit_url(self):
        """Return the absolute url"""
        return ('subscriber_update', [str(self.id)])
    #----------------------------------------------------------------------
    @models.permalink
    def get_delete_url(self):
        """Return the absolute url"""
        return ('subscriber_delete', [str(self.id)])
    #----------------------------------------------------------------------
    def save(self,subscribed=True):
        """Override Save method - subscriber.save(false)"""
        self.subscribed = subscribed
        super(Subscriber,self).save()
    #----------------------------------------------------------------------
    #@models.permalink
    #def get_subscriber_by_email_url(self,email):
        #"""Return the edit url"""
        #return ('subscriber_by_group', [str(self.id)])

########################################################################
class Newsletter(models.Model):
    """Newsletter base"""
    title = models.CharField(max_length=100)
    url = models.URLField()
    content = models.TextField(blank=True)
    view_count = models.IntegerField()
    group = models.ManyToManyField(Group)
    created = models.DateTimeField(blank=False, auto_now_add=True)
    modified = models.DateTimeField(blank=False, auto_now=True)
    #----------------------------------------------------------------------
    def __unicode__(self):
        """return the title field"""
        return self.title
    #----------------------------------------------------------------------
    @models.permalink
    def get_absolute_url(self):
        """Return the absolute url"""
        return ('newsletter_content', [str(self.id)])
        #return "content/" + str(self.id) + "/"
    #----------------------------------------------------------------------
    @models.permalink
    def get_edit_url(self):
        """Return the edit url"""
        #return "/edit/" + str(self.id) + "/"
        return ('newsletter_edit', [str(self.id)])
    #----------------------------------------------------------------------
    @models.permalink
    def get_delete_url(self):
        """Return the delete url"""
        return('newsletter_delete',[str(self.id)])
    #----------------------------------------------------------------------
    def save(self, edit=False, force_insert=False, force_update=False):
        """Override the save function to treat the html content"""
        #if not edit:
            #content = parse(self.url).getroot()
            #content.make_links_absolute()
            #self.content = tostring(content)
            #self.view_count = 0
            #super(Newsletter,self).save(force_insert, force_update)
            #self.save_links()
        #else:
            #q = Newsletter.objects.get(id=self.id)
            #if self.url != q.url:
                #content = parse(self.url).getroot()
                #content.make_links_absolute()
                #self.content = tostring(content)
                #self.view_count = 0
                #super(Newsletter,self).save(force_insert, force_update)
                #self.save_links()
            #else:
                #super(Newsletter,self).save(force_insert, force_update)

        content = parse(self.url).getroot()
        content.make_links_absolute()
        self.content = tostring(content)
        self.view_count = 0
        
        super(Newsletter,self).save(force_insert, force_update)
        self.save_links()
    #----------------------------------------------------------------------
    def save_links(self):
        """This function gets the html at self.content and save all the links at the Link() model"""
        doc = parse(self.url).getroot()

        #WARNING: It's needed a diferent method to find href's, if the user don't use standard newsletter we provide
        count=0
        for el in doc.cssselect('a'):
            count +=1

        if (len(Link.objects.filter(newsletter=self)) != count):
            Link.objects.filter(newsletter=self).delete()

            edit = False #Initialize the link, edit=True will increment it

            import random
            import hashlib

            for el in doc.cssselect('a'):
                if not Link.objects.filter(link=el.get('href'),newsletter=self):
                    rand = str(random.random())
                    salt = hashlib.sha1(rand).hexdigest()[:5]
                    link = Link()
                    link.link = el.get('href')
                    link.newsletter = self
                    link.created_hash = hashlib.sha1(salt+el.get('href')).hexdigest()
                    link.click_count = 0
                    link.label = link.link
                    if link.link == 'http://unsubscribe':
                        link.label = 'unsubscribe'
                    link.save(edit)
                    self.rewrite_html()

    #----------------------------------------------------------------------
    def rewrite_html(self):
        """rewrite the self.content with the newlinks"""
        #import socket
        #host = socket.gethostname()
        from settings import NEWSLETTERS_URL
        links = Link.objects.filter(newsletter=self)
        import re
        for el in links:
            rewrited = re.sub('%s'%(el.link),'%snewsletter/news/%s'%(NEWSLETTERS_URL,el.created_hash),self.content)

        self.content = rewrited
        super(Newsletter,self).save()


########################################################################
class Link(models.Model):
    """Class to store the newsletter links with the corresponding hash"""
    link = models.URLField()
    newsletter = models.ForeignKey(Newsletter)
    created_hash = models.CharField(max_length=60)
    click_count = models.IntegerField(blank=True)
    label = models.CharField(max_length=250)
    #----------------------------------------------------------------------
    def __unicode__(self):
        """return the link hash"""
        return self.link
    #----------------------------------------------------------------------

    def save(self, edit=False, force_insert=False, force_update=False):
        if edit:
            self.click_count += 1
        super(Link, self).save(force_insert, force_update) # Call the "real" save() method.


########################################################################
class Submission(models.Model):
    """Store the letters send date"""
    #group = models.ManyToManyField(Group)
    sent_date = models.DateTimeField(default=datetime.datetime.today)
    newsletter = models.ForeignKey(Newsletter)
    #----------------------------------------------------------------------
    def __unicode__(self):
        """return newsletter name and send date"""
        from django.utils.encoding import smart_unicode
        return smart_unicode(str(self.newsletter), encoding='utf-8', strings_only=False, errors='strict') + self.sent_date.strftime(' %Y %b %d')
    #----------------------------------------------------------------------
    def get_time(self):
        """return the sent date formated"""
        return self.sent_date.strftime('%H:%m - %Y %b %d')

#Talvez criar mais classes para guardar servidores de mail e contar os links por subscritor
