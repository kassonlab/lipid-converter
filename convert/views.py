from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.context_processors import csrf
from forms import ConvertForm
from transform import lipid_converter
from storage import *
from google.appengine.ext import deferred

def main(request):
    return render_to_response('base.html')

def convert(request):    
    if request.POST:
        form = ConvertForm(request.POST,request.FILES)
        
        if form.is_valid():
            
            ff_from = form.cleaned_data['ff_from']
            ff_to = form.cleaned_data['ff_to']
            email = form.cleaned_data['email']
            f  = request.FILES['pdb'].read()
            fn = request.FILES['pdb'].name
            #print ff_from
            #print ff_to
            #print email
            #print f
            save_to_cloud(f,fn)
            
            #form.stat_file(fn)
            #form.list_bucket('/lipid-converter')
            #form.read_file(fn)

            # Here I want to spawn an asynchrouous task and later
            # return the result
            
            deferred.defer(lipid_converter,fn,ff_from,ff_to,email)
            #foo = lipid_converter(fn,ff_from,ff_to)
            #print foo
            # Redirect to a result page after post to avoid duplicates
            return HttpResponseRedirect('/convert/results/%s'%email)
    else:
        form = ConvertForm()

    args = {}
    args.update(csrf(request))
    args['form']=form
    
    return render_to_response('convert.html',args)

def transform(request):
    return render_to_response('transform.html')

def help(request):
    return render_to_response('help.html')

def references(request):
    return render_to_response('references.html')

def results(reuquest,email):
    
    if email[-1]=='/':
        email = email[:-1]
            
    args = {}
    args['email']=email
    return render_to_response('results.html',args)

# There are probably much better ways of doing this
def download(request,file_id):
    
    # is this safe here without any validation?
    if request.method=='POST':
        if file_id[-1]=='/':
            file_id = file_id[:-1]
            
        return HttpResponseRedirect('/convert/get/%s'%file_id)

    args = {}
    args.update(csrf(request))
    args['file_id']=file_id
    
    return render_to_response('download.html',args)

def get(request,file_id):
    
    if file_id[-1]=='/':
        file_id = file_id[:-1]
        
    data = read_file(file_id)
    
    response = HttpResponse(data)
    t = 'text/plain'
    encoding = 'utf-8'
    
    response['Content-Type']=t
    response['Content-Length'] = len(data)

    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        filename_header = 'filename=result.gro'
    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        filename_header = ''
    else:
        filename_header = 'filename*=UTF-8\'\'result.gro'
    response['Content-Disposition'] = 'attachment; ' + filename_header

    return response
