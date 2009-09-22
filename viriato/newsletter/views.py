# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from newsletter.models import Subscriber,Group,Newsletter,Link
from django.db.models import Q
from newsletter.forms import NewsletterForm, LinkFormset, UnsubscribeForm
from django.views.generic.create_update import create_object, update_object
from django.views.generic import list_detail

import httplib2, urllib2, lxml
from lxml.html import fromstring, iterlinks, make_links_absolute
from settings import ROOT_DIR, PROJECT_ROOT

from django.core import serializers #added by Emanuel


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
        form = NewsletterForm(request.POST, instance=newsletter)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/newsletter/')
    else:
        #formset = BookInlineFormSet(instance=author)
        form = NewsletterForm(instance=newsletter)
    return render_to_response("newsletter/newsletter_edit.html",
                              {"form": form,"newsletter":newsletter},
                              context_instance=RequestContext(request))

#----------------------------------------------------------------------
def newsletter_analytics(request,newsletter_id):
    newsletter = get_object_or_404(Newsletter,id=newsletter_id)
    #import simplejson as json Acho q não é preciso
    #l = Link.objects.get(newsletter=newsletter)
    #dict = newsletter.get_links() não é preciso
    #print dict
    #js_data = json.dumps(dict, separators=(',',':'))
    #return render_to_response('newsletter/newsletter_analytics.html',
                              #{'newsletter' : newsletter,'js_data':js_data},
                              #context_instance=RequestContext(request))
    return render_to_response('newsletter/newsletter_analytics.html',
                              {'newsletter' : newsletter,},
                              context_instance=RequestContext(request))

def links_ajax(request, newsletter_id):
    #Created by Emanuel
    data = serializers.serialize('json', Link.objects.filter(newsletter= newsletter_id), ensure_ascii=False)
    return HttpResponse(data,mimetype='text/javascript')

#----------------------------------------------------------------------
def newsletter_send(request, object_id):
    path = PROJECT_ROOT + "/core/scripts/sendmail_v0.1.py"
    print path
    #try:
        #newsletter = Newsletter.objects.get(id=newsletter_id)
    #except Newsletter.DoesNotExist:
        #raise Http404
    import sys, subprocess, os
    #os.system  = path +' -n 1'
    #sys.stderr.write(ROOT_DIR + '/sendmail_v0.1.py -n 1')
    #p = subprocess.Popen([sys.executable, path  +'-n 1'],
                                    #stdout=subprocess.PIPE,
                                    #stderr=subprocess.STDOUT)
    #sys.executable("%s -n 1"%path)

    #return HttpResponseRedirect('/newsletter/')
    newsletter = get_object_or_404(Newsletter,id=object_id)
    #from subprocess import call
    #retcode = call([path , "-n %s"%str(object_id)])
    #os.system('python '+path+ ' -n 1')
    os.system('python %s -n %s'%(path,str(object_id)))
    return render_to_response('newsletter/newsletter_content.html',
                              {'newsletter' : newsletter},
                              context_instance=RequestContext(request))

#----------------------------------------------------------------------
def manage_links(request, object_id):
    from django.forms.models import inlineformset_factory

    newsletter = Newsletter.objects.get(pk=object_id)
    if request.method == "POST":
        formset = LinkFormset(request.POST, request.FILES, instance=newsletter)
        if formset.is_valid():
            formset.save()
            # Do something.
    else:
        formset = LinkFormset(instance=newsletter)

    return render_to_response("newsletter/manage_links.html",
                              {"formset": formset,},
                              context_instance=RequestContext(request))

#----------------------------------------------------------------------
def subscriber_by_group(request, object_id):
    """It sorts subscribers by group"""
    #look up the group
    #try:
    grp = Group.objects.get(id=object_id)
    #except Group.DoesNotExist:
       #raise Http404

    return list_detail.object_list(
        request,
        queryset = Subscriber.objects.filter(group = grp),
        template_name = "newsletter/subscriber_by_group.html",
        extra_context = {"group_list": Group.objects.all}
        )

#----------------------------------------------------------------------
def link_count(request,link_hash):
    """Count click hits"""
    edit = True
    link = Link.objects.get(created_hash = link_hash)
    link.save(edit)
    if link.slug == 'unsubscribe':
        if request.method == 'POST':
            form = UnsubscribeForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                subscriber = get_object_or_404(Subscriber,email=email)
                subscriber.save(False)
                return render_to_response("newsletter/unsubscribe_tks.html")
        else:
                form = UnsubscribeForm()
                return render_to_response("newsletter/unsubscribe.html",
                                {"form":form,},
                                context_instance=RequestContext(request))
    else:
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