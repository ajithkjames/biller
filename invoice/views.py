# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.template import loader, Context, RequestContext
import datetime
import dateutil.parser
import easy_pdf
from easy_pdf.views import PDFTemplateView
import json
from num2words import num2words

# Create your views here.
class Home(TemplateView):
    template_name = "home.html"


class PDFView(PDFTemplateView):
    template_name = "hello.html"
    def post(self,request, *args, **kwargs):
    	filename='invoice.pdf'
    	data = json.loads(request.body)
        products= data.get('items', None)
        count= len(products)
        num= 15-count
        date=dateutil.parser.parse(data.get('date', None))
        due=dateutil.parser.parse(data.get('due', None))
        wordtotal=num2words(data.get('grandtotal'))
    	context={
    	'loop_times' : range(1, num),
    	'number':data.get('number', None),
    	'date':date,
    	'due':due,
    	'from_text':data.get('from_text', None),
    	'to_text':data.get('to_text', None),
    	'from':data.get('company'),
    	'to':data.get('customer'),
    	'logo': data.get('logo', None),
    	'items': data.get('items', None),
    	'subtotal':data.get('subtotal', None),
    	'taxtitle':data.get('taxtitle'),
    	'tax':data.get('tax'),
    	'taxamount':data.get('taxamount'),
    	'taxtitle1':data.get('taxtitle1'),
    	'tax1':data.get('tax1'),
    	'taxamount1':data.get('taxamount1'),
    	'grandtotal':data.get('grandtotal'),
    	'notes':data.get('notes'),
    	'terms':data.get('terms'),
    	'currency':data.get('currency'),
    	'additionaltax':data.get('additionaltax'),
        'wordtotal':wordtotal,
    	}
    	return easy_pdf.rendering.render_to_pdf_response(request, template=self.template_name, context=context, filename=filename, encoding=u'utf-8')
    	

class send(View):

    def post(self,request, *args, **kwargs):
		products= request.data.get('items', None)
		count= len(products)
		num= 15-count
		date=dateutil.parser.parse(request.data.get('date', None))
		due=dateutil.parser.parse(request.data.get('due', None))
		to=request.data.get('to', None)
		sender =request.data.get('from', None)
		message =request.data.get('message', None)
		context={
		'loop_times' : range(1, num),
    	'number':request.data.get('number', None),
    	'date':date,
    	'due':due,
    	'from_text':request.data.get('from_text', None),
    	'to_text':request.data.get('to_text', None),
    	'from':request.data.get('company'),
    	'to':request.data.get('customer'),
    	'logo': request.data.get('logo', None),
    	'items': request.data.get('items', None),
    	'subtotal':request.data.get('subtotal', None),
    	'taxtitle':request.data.get('taxtitle'),
    	'tax':request.data.get('tax'),
    	'taxamount':request.data.get('taxamount'),
    	'taxtitle1':request.data.get('taxtitle1'),
    	'tax1':request.data.get('tax1'),
    	'taxamount1':request.data.get('taxamount1'),
    	'grandtotal':request.data.get('grandtotal'),
    	'notes':request.data.get('notes'),
    	'terms':request.data.get('terms'),
    	'currency':request.data.get('currency'),
    	'additionaltax':request.data.get('additionaltax'),
    	}
		filestr1 = loader.render_to_string("pdf.html", context)
		filestr = easy_pdf.rendering.html_to_pdf(content=filestr1, encoding=u'utf-8')

		try:
			email = EmailMessage(
			'Invoice from '+sender,
			message,
			"Invoice Generator",
			[to],
			headers={'Message-ID': 'foo'},
			)
			email.attach('invoice.pdf', filestr, 'application/pdf')
			email.send()
		except BadHeaderError:
			return HttpResponse('Invalid header found.')
		return HttpResponse('success')
