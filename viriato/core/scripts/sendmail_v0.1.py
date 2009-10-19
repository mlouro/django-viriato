#!/usr/bin/env python
#coding:utf-8
# Author:   --< Coin >
# Purpose: sendmail 0.1
# Created: 19-04-2009

__version__ = "0.1"
__author__ = "Coin"
__license__ = "ClickVision"

import sys,os
from optparse import OptionParser

usage = "usage: %prog -n NEWSLETTER | --newsletter=NEWSLETTER"
parser = OptionParser(usage)
parser.add_option('-n', '--newsletter', dest='newsletter', metavar='NEWSLETTER', help="The Newsletter ID to use")
(options, args) = parser.parse_args()
if not options.newsletter:
    parser.error("You must specifiy a Newsletter ID")

sys.path.append('/opt/webapps/viriato.reactivelab.com/src/viriato-trunk/viriato, /opt/webapps/viriato.reactivelab.com/lib/python2.6/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] ='viriato.settings'

from django.core.management import setup_environ
import settings

setup_environ(settings)

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

########################################################################
class mailx:
    """Mailx class"""
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.mail= MIMEMultipart('alternative')
    #----------------------------------------------------------------------
    def htmlprep(self,subject,alias,html):
        """It attach the newsletter to the  mail instance """ 

        self.mail['Subject'] = subject
        self.mail['From'] = alias
        content_text = MIMEText("If you are reading this the newsletter didn't load correctly", 'text')
        content_html = MIMEText(html, 'html')

        self.mail.attach(content_text)
        self.mail.attach(content_html)

    #----------------------------------------------------------------------
    def sendmail(self,server,port,to,user,pwd):
        """Send mail Function"""
        self.mailServer = smtplib.SMTP(server, port)
        self.mailServer.ehlo()
        self.mailServer.starttls()
        self.mailServer.ehlo()
        self.mailServer.login(user,pwd)
        #self.mailServer.set_debuglevel(1)
        for el in to:
            try:
                self.mailServer.sendmail(user,el.email,self.mail.as_string())
                print '========\n\nSENT TO %s - %s\n\n========'%(el.name,el.email)
            except Exception, e:
                print e
                raise
        self.mailServer.close()
        
########################################################################


if __name__ == "__main__":
    from newsletter.models import Subscriber,Group,Newsletter
    from django.db.models import Q
    
    newsletter = Newsletter.objects.get(id=options.newsletter)
    html = newsletter.content
    subject =  newsletter.title
    
    to = []
    groups=[]
    
    for gr in newsletter.group.all():
        groups.append(gr)
        for subs in Subscriber.objects.filter(Q(group=gr)):
            if not subs in to and subs.subscribed == True:
                to.append(subs)
        
    server = "smtp.gmail.com"
    #port = 587
    port = 25
    
    gmail_user = "viriatoletter@gmail.com"   #Username
    gmail_pwd  = "<alexandre>"                   #Password
    gmail_alt  = "Viriato"                               #Alias ID
    gmail_alias = "Newsletter "+gmail_alt   #nickname
    
    #mailto   =  ' ',' '
    #mailtoBcc=  ' '
    
    
    ########################################################################
    newmail = mailx()
    
    #newmail.mailprep(gmail_alias,subject)
    newmail.htmlprep(subject,gmail_alias,html)
    #for el in to:
    newmail.sendmail(server,port,to,gmail_user,gmail_pwd)
        #print 'Sent to %s - %s'%(el.name,el.email)
        
        
        
        
        
