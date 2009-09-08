from django.db import models
import datetime
from lxml.html import parse, iterlinks, make_links_absolute,tostring

########################################################################
class Group(models.Model):
    """Groups data"""
    name = models.CharField(blank = False, unique=True, max_length=60)
    created = models.DateTimeField(blank=False, auto_now_add=True)
    modified = models.DateTimeField(blank=False, auto_now=True)
    #----------------------------------------------------------------------
    def __unicode__(self):
        """return de group name"""
        return self.name
    #----------------------------------------------------------------------
    def get_subscribers_by_group_url(self):
        """Return the filter url"""
        return "/newsletter/subscribers-by-group/" + str(self.id) + "/"

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
    def get_absolute_url(self):
        """Return the absolute url"""
        return "subscriber-content/" + str(self.id) + "/"
    #----------------------------------------------------------------------
    def get_edit_url(self):
        """Return the edit url"""
        return "/newsletter/subscriber-update/" + str(self.id) + "/"

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
    def get_absolute_url(self):
        """Return the absolute url"""
        return "newsletter-content/" + str(self.id) + "/"
    #----------------------------------------------------------------------
    def get_edit_url(self):
        """Return the edit url"""
        return "/newsletter/newsletter-edit/" + str(self.id) + "/"
    #----------------------------------------------------------------------
    def save(self):
        """Override the save function to treat the html content"""
        content = parse(self.url).getroot()
        content.make_links_absolute()
        self.content = tostring(content)
        self.view_count = 0

        super(Newsletter,self).save()
        """save links"""
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
                    link.slug = link.link
                    if link.link == 'http://unsubscribe':
                        link.slug = 'unsubscribe'
                    link.save(edit)
                    self.rewrite_html()

            #for el in doc.cssselect('a'):
                #if not el.get('href') == 'http://unsubscribe':
                    #rand = str(random.random())
                    #salt = hashlib.sha1(rand).hexdigest()[:5]
                    #link = Link()
                    #link.link = el.get('href')
                    #link.newsletter = self
                    #link.created_hash = hashlib.sha1(salt+el.get('href')).hexdigest()
                    #link.click_count = 0
                    #link.save(edit)
                    #self.rewrite_html()
                #else:
                    #if not Link.objects.filter(link='http://unsubscribe'):
                        #rand = str(random.random())
                        #salt = hashlib.sha1(rand).hexdigest()[:5]
                        #link = Link()
                        #link.link = el.get('href')
                        #link.newsletter = self
                        #link.created_hash = hashlib.sha1(salt+el.get('href')).hexdigest()
                        #link.click_count = 0
                        #link.save(edit)
                        #self.rewrite_html()

    #----------------------------------------------------------------------
    def rewrite_html(self):
        """rewrite the self.content with the newlinks"""
        import socket
        host = socket.gethostname()
        links = Link.objects.filter(newsletter=self)
        import re
        for el in links:
            rewrited = re.sub('%s'%(el.link),'http://%s:8000/newsletter/news/%s'%(host,el.created_hash),self.content)
            #if not el.link == 'http://unsubscribe':
                #rewrited = re.sub('%s'%(el.link),'http://%s:8000/newsletter/news/%s'%(host,el.created_hash),self.content,1)
            #else:
                #rewrited = re.sub('%s'%(el.link),'http://%s:8000/newsletter/news/%s'%(host,el.created_hash),self.content)
        self.content = rewrited
        super(Newsletter,self).save()

    #----------------------------------------------------------------------
    def chart_links(self):
        """"""
        from pychartdir import *

        links = Link.objects.filter(newsletter = self)
        data = []
        labels = []
        for el  in links:
            # The data for the bar chart
            data.append(el.click_count)
            # The labels for the bar chart
            labels.append(str(el.slug))
        #print "QQQQQQQQQQQQQQQQQQQQQQ"
        #print len(links)

        #switch len(links):
            #case =5:
                #print "Igual"
            #case <5:
                #print "Menor"
            #else:
                #print "NADA"

        # Create a XYChart object of size 600 x 250 pixels
        c = XYChart(600, 250)

        # Add a title to the chart using Arial Bold Italic font
        c.addTitle("Newsletter %s " % str(self.title), "arialbi.ttf")

        # Set the plotarea at (100, 30) and of size 400 x 200 pixels. Set the plotarea
        # border, background and grid lines to Transparent
        c.setPlotArea(200, 30, 400, 100, Transparent, Transparent, Transparent, Transparent,
                      Transparent)

        # Add a bar chart layer using the given data. Use a gradient color for the bars,
        # where the gradient is from dark green (0x008000) to white (0xffffff)
        layer = c.addBarLayer(data, c.gradientColor(100, 0, 800, 0, 0x008000, 0xffffff))

        # Swap the axis so that the bars are drawn horizontally
        c.swapXY(1)

        # Set the bar gap to 10%
        layer.setBarGap(0.1)

        # Use the format "xxx Clicks" as the bar label
        layer.setAggregateLabelFormat("{value} Clicks")

        # Set the bar label font to 10 pts Arial Bold Italic/dark red (0x663300)
        layer.setAggregateLabelStyle("arialbi.ttf", 10, 0x663300)

        # Set the labels on the x axis
        textbox = c.xAxis().setLabels(labels)

        # Set the x axis label font to 10pt Arial Bold Italic
        textbox.setFontStyle("arialbi.ttf")
        textbox.setFontSize(10)

        # Set the x axis to Transparent, with labels in dark red (0x663300)
        c.xAxis().setColors(Transparent, 0x663300)

        # Set the y axis and labels to Transparent
        c.yAxis().setColors(Transparent, Transparent)

        # Output the chart
        path = "static/images/tmp/tmpcharts/hbar.png"
        c.makeChart(path)

        return path

########################################################################
class Link(models.Model):
    """Class to store the newsletter links with the corresponding hash"""
    link = models.URLField()
    newsletter = models.ForeignKey(Newsletter)
    created_hash = models.CharField(max_length=60)
    click_count = models.IntegerField(blank=True)
    slug = models.SlugField()
    #----------------------------------------------------------------------
    def __unicode__(self):
        """return the link hash"""
        return self.link
    #----------------------------------------------------------------------
    def save(self,edit):
        """save(self,edit=True) will increment the click_count field
        save(self,edit=False ) will save a new object with the click_count=0"""

        if edit:
            self.click_count += 1
        super(Link,self).save()

    #----------------------------------------------------------------------
    def chart_test(self):
        """"""
        from pychartdir import *

        # The data for the bar chart
        data = [450, 560, 630, 800, 1100, 1350, 1600, 1950, 2300, 2700]

        # The labels for the bar chart
        labels = ["1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004",
                  "2005"]

        # Create a XYChart object of size 600 x 360 pixels
        c = XYChart(600, 360)

        # Add a title to the chart using 18pts Times Bold Italic font
        c.addTitle("Annual Revenue for Star Tech", "timesbi.ttf", 18)

        # Set the plotarea at (60, 40) and of size 500 x 280 pixels. Use a vertical gradient
        # color from light blue (eeeeff) to deep blue (0000cc) as background. Set border and
        # grid lines to white (ffffff).
        c.setPlotArea(60, 40, 500, 280, c.linearGradientColor(60, 40, 60, 280, 0xeeeeff,
                                                              0x0000cc), -1, 0xffffff, 0xffffff)

        # Add a multi-color bar chart layer using the supplied data. Use soft lighting effect
        # with light direction from top.
        c.addBarLayer3(data).setBorderColor(Transparent, softLighting(Top))

        # Set x axis labels using the given labels
        c.xAxis().setLabels(labels)

        # Draw the ticks between label positions (instead of at label positions)
        c.xAxis().setTickOffset(0.5)

        # When auto-scaling, use tick spacing of 40 pixels as a guideline
        c.yAxis().setTickDensity(40)

        # Add a title to the y axis with 12pts Times Bold Italic font
        c.yAxis().setTitle("USD (millions)", "timesbi.ttf", 12)

        # Set axis label style to 8pts Arial Bold
        c.xAxis().setLabelStyle("arialbd.ttf", 8)
        c.yAxis().setLabelStyle("arialbd.ttf", 8)

        # Set axis line width to 2 pixels
        c.xAxis().setWidth(2)
        c.yAxis().setWidth(2)

        # Create the image and save it in a temporary location
        chart1URL = c.makeTmpFile("/tmp/tmpcharts")

        # Create an image map for the chart
        imageMap = c.getHTMLImageMap("clickline.py", "", "title='{xLabel}: US$ {value|0}M'")

########################################################################
class Submission(models.Model):
    """Store the letters send date"""
    newsletter = models.ForeignKey(Newsletter)
    group = models.ManyToManyField(Group)
    sent_date = models.DateTimeField("Sent date")

    #----------------------------------------------------------------------
    def __unicode__(self):
        """return newsletter name and send date"""
        return self.newsletter + ' ' + self.send_date

#Talvez criar mais classes para guardar servidores de mail e contar os links por subscritor