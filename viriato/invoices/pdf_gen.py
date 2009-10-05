# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import Table
from reportlab.lib.colors import *
from django.utils.translation import ugettext as _

def set_states(c, author='Emanuel', title='My Document'):
    c.setPageSize(A4)
    c.translate(0,0)
    c.saveState()
    c.setAuthor(author)
    c.setTitle(title)

def create_header(c, instance):
    w, h = A4
    c.beginForm("header")
    c.drawImage('static/%s' % (str(instance.photo)), x= w-inch, y= h-inch,width=50, height=50)
    content = []
    s1 = _('Company')
    s2 = instance.title
    content.append ('%s: %s' % (s1,s2))
    s1 = 'Nif'
    s1 = instance.nif
    content.append ('%s: %s' %(s1, s2))
    p = c.beginText()
    p.setTextOrigin(x= inch, y= h-inch)
    for line in content:
        p.textLine(line)
    c.drawText(p)
    p = c.beginPath()
    c.setStrokeColor(blue)
    p.moveTo(inch, h - inch * 1.5)
    p.lineTo(w-inch, h - inch * 1.5)
    c.drawPath(p, fill=1, stroke=1)
    c.endForm()
    c.doForm("header")

def create_footer(c, instance):
    w, h = A4
    c.beginForm("footer")
    p = c.beginPath()
    c.setStrokeColor(blue)
    p.moveTo(inch, inch)
    p.lineTo(w-inch, inch)
    c.drawPath(p, fill=1, stroke=1)
    content = []
    s2 = instance.title
    content.append ('%s' % (s2))
    s1 = _('Visit at')
    s2 = ('www.viriato.com') # need to be updated
    content.append ('%s: %s' % (s1, s2))
    p = c.beginText()
    p.setTextOrigin(x= inch, y= inch * 0.8)
    for line in content:
        p.textLine(line)
    c.drawText(p)
    c.endForm()
    c.doForm('footer')

def create_doc_main(c, object_id, instance, receipt=True):
    w, h = A4
    content = []
    if receipt:
        s1 = _('Receipt nr.')
    else:
        s1 = _('Contract nr.')
    content.append('%s: %s' % (s1, object_id))

    client = instance.company.title
    s1 = _('Client')
    content.append('%s: %s' % (s1, client))

    p = c.beginText()
    p.setTextOrigin(x= inch, y= h - inch * 2)
    for line in content:
        p.textLine(line)
    c.drawText(p)

def create_doc_details(c, instance, details_instance):
    w, h = A4
    document_details = []

    c.setFont("Helvetica", 8)

    table_header = [_('Description'),'','', '', '', _('Quantity'), _('Unity Cost'), _('Imp. Value'), _('Tax'), _('Tax Value'), _('Retention'), _('Ret. Value'), _('Total')]
    for rd in details_instance:
        new_data = [rd.description[:50],'','','','', rd.quantity, rd.unity_cost, rd.total_impact_value, rd.tax, rd.tax_value, rd.retention, rd.retention_value, rd.total]
    table_footer = [_('Totals'),'', ' ' ,'',' ', ' ', ' ', instance.total_impact_value, ' ', instance.total_tax_value, ' ',instance.total_retention_value, instance.total]


    document_details.append(table_header)
    document_details.append(table_footer)


        document_details.append(new_data)





    ts = [
            ('FONT', (0,0), (-1,-1), 'Times-Roman', 8),
            ('ALIGN', (1,1), (-1,-1), 'CENTER'),
            ('LINEABOVE', (0,0), (-1,0), 1, purple),
            ('LINEBELOW', (0,0), (-1,0), 1, purple),
            ('FONT', (0,0), (-1,0), 'Times-Bold', 6),
            ('LINEABOVE', (0,-1), (-1,-1), 1, purple),
            ('LINEBELOW', (0,-1), (-1,-1), 0.5, purple,1, None, None, 4,1),
            ('LINEBELOW', (0,-1), (-1,-1), 1, red),
            ('FONT', (0,-1), (-1,-1), 'Times-Bold'  ),
        ]
    table = Table(document_details, style=ts, colWidths=35)
    aW = w
    aH = h
    w1,h1 = table.wrap(aW, aH)# find required
    if w<=aW and h<=aH:
        table.drawOn(c, inch ,h - h1 - inch*2.5 )
    else:
        raise ValueError, "Not enough room"