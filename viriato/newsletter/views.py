from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from newsletter.models import Subscriber,Group,Newsletter,Link
from django.db.models import Q
from newsletter.forms import NewsletterForm
from django.views.generic.create_update import create_object, update_object
from django.views.generic import list_detail

import httplib2, urllib2, lxml
from lxml.html import fromstring, iterlinks, make_links_absolute
from settings import ROOT_DIR

def index(request):
    """Present the index newsletter page 
    and send the newsletter data to the template """
    newsletter_list = Newsletter.objects.all().order_by('-created')

    return render_to_response('newsletter/newsletter_list.html',
                              {'newsletter' : newsletter_list},
                              context_instance=RequestContext(request))

#----------------------------------------------------------------------
def newsletter_content(request,newsletter_id):
    """return the newsletter content"""
    newsletter = get_object_or_404(Newsletter,id=newsletter_id)
    
    #l = Link.objects.get(newsletter=newsletter)


    return render_to_response('newsletter/newsletter_content.html',
                              {'newsletter' : newsletter},
                              context_instance=RequestContext(request))

#----------------------------------------------------------------------
def newsletter_add(request):
    if request.method == 'POST':
        formset = NewsletterForm(request.POST)
        print formset.errors
        if formset.is_valid():
            formset.save()
            
            return HttpResponseRedirect('/newsletter/')
        else:
            return render_to_response('newsletter/newsletter_add.html',
                                    {'form' : formset},
                                    context_instance=RequestContext(request))
    else:
        return render_to_response('newsletter/newsletter_add.html',
                                {'form'    : NewsletterForm()},
                                context_instance=RequestContext(request))

#----------------------------------------------------------------------
def newsletter_edit(request, newsletter_id):
    newsletter = Newsletter.objects.get(id=newsletter_id)
    #BookInlineFormSet = inlineformset_factory(Author, Book)
    if request.method == "POST":
        #formset = BookInlineFormSet(request.POST, request.FILES, instance=author)
        formset = NewsletterForm(request.POST, instance=newsletter) 
        if formset.is_valid():
            formset.save()
            
            return HttpResponseRedirect('/newsletter/')
    else:
        #formset = BookInlineFormSet(instance=author)
        formset = NewsletterForm(instance=newsletter)
    return render_to_response("newsletter/newsletter_edit.html", 
                              {"form": formset},
                              context_instance=RequestContext(request))

#----------------------------------------------------------------------
def newsletter_analytics(request,newsletter_id):
    newsletter = get_object_or_404(Newsletter,id=newsletter_id)
    
    #l = Link.objects.get(newsletter=newsletter)

    return render_to_response('newsletter/newsletter_analytics.html',
                              {'newsletter' : newsletter,},
                              context_instance=RequestContext(request))

#----------------------------------------------------------------------
def newsletter_send(request, newsletter_id):
    #try:
        #newsletter = Newsletter.objects.get(id=newsletter_id)
    #except Newsletter.DoesNotExist:
        #raise Http404
    import sys, subprocess, os
    sys.executable  = ROOT_DIR + '/newsletters/sendmail_v0.1.py -n 1'
    #sys.stderr.write(ROOT_DIR + '/sendmail_v0.1.py -n 1')
    #p = subprocess.Popen([sys.executable, ROOT_DIR + '/newsletters/sendmail_v0.1.py -n 1'], 
     #                               stdout=subprocess.PIPE, 
     #                               stderr=subprocess.STDOUT)
    #sys.executable("/home/coin/projects/newsletters-trunk/newsletters/sendmail_v0.1.py -n 1")

    #return HttpResponseRedirect('/newsletter/')
    newsletter = get_object_or_404(Newsletter,id=newsletter_id)

    return render_to_response('newsletter/content.html',
                              {'newsletter' : newsletter},
                              context_instance=RequestContext(request))

#----------------------------------------------------------------------
def subscribers_by_group(request, object_id):
    """It sorts subscribers by group"""
    #look up the group
    #ry:
    grp = Group.objects.get(id=object_id)
    #except Group.DoesNotExist:
       #raise Http404
    
    return list_detail.object_list(
        request,
        queryset = Subscriber.objects.filter(group = grp),
        template_name = "newsletter/subscriber_list.html",
        extra_context = {"group_list": Group.objects.all()}
        )

#----------------------------------------------------------------------
def link_count(request,link_hash):
    """Count click hits"""
    edit = True
    link = Link.objects.get(created_hash = link_hash)
    link.save(edit)
    print link.link
    return HttpResponseRedirect(link.link)

#----------------------------------------------------------------------
def search(request):

    query = request.GET.get('query','')
    results = Subscriber.objects.all()

    if query:
        qset = (Q(title__icontains=query))
        results = Newsletter.objects.filter(qset).distinct()

    return render_to_response("newsletter/index.html",
        { "results": results, "query": query },
        context_instance=RequestContext(request))
#----------------------------------------------------------------------
def host(request):
    #return HttpResponse(request.META['HTTP_HOST'])
    import socket
    host = socket.gethostname()
    return HttpResponse(host)
#----------------------------------------------------------------------
def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

