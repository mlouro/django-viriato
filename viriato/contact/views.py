# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from contact.forms import *
from contact.models import Person, Contact, Website, Address, Email
#from note.models import Note
#from log.models import Log
from django.db.models import Q

@login_required
def save(request, contact_type, contact_id = None):

    if contact_id:
        person = Person.objects.get(id=contact_id)
    else:
        person = Person()

    person_form = PersonForm(instance=person)

    if request.method == 'POST':

        person_form = PersonForm(request.POST)

        if person_form.is_valid():
            person = person_form.save(commit=False)
            if contact_id:
                person.id = contact_id
            person.save()

            #if contact_id:
                #person.logs.create(log="Updated contact " + person.first_name + " " + #person.last_name,user=request.user)
            #else:
                #person.logs.create(log="Added contact " + person.first_name + " " + person.last_name,user=request.user)

        formset_list = {'email_formset' : EmailFormSet(instance=person,data=request.POST),
                    'phone_formset' : PhoneFormSet(instance=person,data=request.POST),
                    'im_formset' : InstantMessagingFormSet(instance=person,data=request.POST),
                    'address_formset' : AddressFormSet(instance=person,data=request.POST),
                    'website_formset' : WebsiteFormSet(instance=person,data=request.POST),}

        for formset in formset_list:
            #print formset_list[formset].is_valid()
            if formset_list[formset].is_valid():
                formset_list[formset].save()
                formset_list[formset] = type(formset_list[formset])(instance=person)

    else:
        formset_list = {'email_formset' : EmailFormSet(instance=person),
                    'phone_formset' : PhoneFormSet(instance=person),
                    'im_formset' : InstantMessagingFormSet(instance=person),
                    'address_formset' : AddressFormSet(instance=person),
                    'website_formset' : WebsiteFormSet(instance=person),}

    return render_to_response('contacts/save.html',
                               { 'form' : person_form,
                                 'person' : person,
                                 'formsets' : formset_list, },
                               context_instance=RequestContext(request)
                            )

@login_required
def search(request):

    query = request.GET.get('query', '')
    results = Person.objects.all()

    if query:
        qset = (Q(first_name__icontains=query) | Q(last_name__icontains=query))
        results = Person.objects.filter(qset).distinct()

    return render_to_response("contacts/index.html",
        { "results": results, "query": query },
        context_instance=RequestContext(request))



@login_required
def details(request,contact_type,contact_id):

    entity = Person.objects.get(id=contact_id)

    return render_to_response("contacts/details.html",
        { "entity": entity,
         "notes": entity.notes.all().order_by("-created"), },
        context_instance=RequestContext(request))


#@login_required
#def addnote(request,contact_type,contact_id):

    #if contact_type == "person":
        #entity = Person.objects.get(id=request.POST['entity_id'])

    #note = entity.notes.create(note=request.POST['note'],user=request.user)

    #if note:
        #note.logs.create(log="Added a note to " + entity.first_name + " " + entity.last_name, user=request.user)

    #return render_to_response("contacts/details.html",
        #{ "entity": entity,
         #"notes": entity.notes.all().order_by("-created"), },
        #context_instance=RequestContext(request))