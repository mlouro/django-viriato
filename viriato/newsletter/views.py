# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from newsletter.models import Subscriber,Group,Newsletter,Link
from django.db.models import Q
from newsletter.forms import NewsletterForm, LinkFormset, UnsubscribeForm
from django.views.generic.create_update import create_object, update_object
from django.views.generic import list_detail
from django.contrib.auth.decorators import login_required, permission_required

import httplib2, urllib2, lxml
from lxml.html import fromstring, iterlinks, make_links_absolute
from settings import ROOT_DIR, PROJECT_ROOT

from django.core import serializers #added by Emanuel

@login_required
def index(request):
    """Present the index newsletter page
    and send the newsletter data to the template """
    newsletter_list = Newsletter.objects.all().order_by('-created')

    return render_to_response('newsletter/newsletter_list.html',
                              {'newsletter' : newsletter_list},
                              context_instance=RequestContext(request))

#----------------------------------------------------------------------
@login_required
def newsletter_content(request,newsletter_id):
    """return the newsletter content"""
    newsletter = get_object_or_404(Newsletter,id=newsletter_id)

    #l = Link.objects.get(newsletter=newsletter)

    return render_to_response('newsletter/newsletter_content.html',
                              {'newsletter' : newsletter},
                              context_instance=RequestContext(request))

#----------------------------------------------------------------------
@login_required
def newsletter_add(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)

        if form.is_valid():
            #newsl = 
            form.save()

            #return HttpResponseRedirect('/newsletter/edit/%s'%(newsl.id))
            return HttpResponseRedirect('/newsletter/list')
        else:
            return render_to_response('newsletter/newsletter_add.html',
                                    {'form' : form},
                                    context_instance=RequestContext(request))
    else:
        return render_to_response('newsletter/newsletter_add.html',
                                {'form': NewsletterForm()},
                                context_instance=RequestContext(request))

#----------------------------------------------------------------------
@login_required
def newsletter_edit(request, newsletter_id):
    #from django.forms.models import inlineformset_factory
    
    newsletter = Newsletter.objects.get(id=newsletter_id)
    if request.method == "POST":
        form = NewsletterForm(request.POST, instance=newsletter)
        #form = NewsletterForm(request.POST, instance=newsletter, prefix="newsletter")
        #formset = LinkFormset(request.POST, request.FILES, instance=newsletter, prefix="links")
        if form.is_valid():
        #and formset.is_valid():
            #f = form.save(commit=False)
            #f.save(True)
            #form.save_m2m()
            #formset.save()
            form.save()
            
            return HttpResponseRedirect('/newsletter/edit/%s'%(newsletter_id))
    else:
        form = NewsletterForm(instance=newsletter)
        #form = NewsletterForm(instance=newsletter, prefix="newsletter")
        #formset = LinkFormset(instance=newsletter, prefix="links")
        
    return render_to_response("newsletter/newsletter_edit.html",
                              {"form": form,"newsletter":newsletter,
                               #"formset": formset,
                               },
                              context_instance=RequestContext(request))

#----------------------------------------------------------------------
@login_required
def manage_links(request, object_id):
    from django.forms.models import inlineformset_factory

    newsletter = Newsletter.objects.get(pk=object_id)
    if request.method == "POST":
        formset = LinkFormset(request.POST, request.FILES, instance=newsletter)
        if formset.is_valid():
            formset.save()

        else:
            return render_to_response("newsletter/manage_links.html",
                              {"formset": formset,
                                "object_id": object_id,},
                              context_instance=RequestContext(request))
    else:
        formset = LinkFormset(instance=newsletter)

    return render_to_response("newsletter/manage_links.html",
                              {"formset": formset,
                                "object_id": object_id,
                                "newsletter":newsletter},
                              context_instance=RequestContext(request))

#----------------------------------------------------------------------
@login_required
def newsletter_analytics(request,newsletter_id):
    newsletter = get_object_or_404(Newsletter,id=newsletter_id)

    return render_to_response('newsletter/newsletter_analytics.html',
                              {'newsletter' : newsletter,},
                              context_instance=RequestContext(request))

#----------------------------------------------------------------------
def links_ajax(request):
    #Created by Emanuel
    newsletter_id = int(request.POST['newsletter_id'])
    data = serializers.serialize('json', Link.objects.filter(newsletter=newsletter_id), ensure_ascii=False)
    return HttpResponse(data,mimetype='application/json')

#----------------------------------------------------------------------
def dashboard_ajax(request):

    aux =[]
    info=[]
    for el in Link.objects.all():
        if not el.link == 'http://unsubscribe':
            if not el.link in aux:
                aux.append(el.link)
                cont=0
                for obj in Link.objects.filter(Q(link=el.link)):
                    cont += obj.click_count
                el.click_count=cont
                info.append(el)

    print info
    data = serializers.serialize('json', info, ensure_ascii=False)
    return HttpResponse(data,mimetype='text/javascript')

#----------------------------------------------------------------------
@login_required
def newsletter_send(request, object_id):
    import os

    path = PROJECT_ROOT + "/core/scripts/sendmail_v0.1.py"
    newsletter = get_object_or_404(Newsletter,id=object_id)

    os.system('python %s -n %s'%(path,str(object_id)))
    
    from newsletter.models import Submission

    sub = Submission(newsletter=newsletter)
    sub.save()

    return render_to_response('newsletter/newsletter_content.html',
                              {'newsletter' : newsletter},
                              context_instance=RequestContext(request))

#----------------------------------------------------------------------
@login_required
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
    if link.label == 'unsubscribe':
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
        {"results": results, "query": query },
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