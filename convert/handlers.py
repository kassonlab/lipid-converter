import os
import cgi
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.ext import deferred
from storage import *
#from lipid_converter import lipid_converter_transform
#from lipid_converter import lipid_converter_convert
from lipid_converter import T
from lipid_converter import C
import gcs_data
import logging
import re

class BaseHandler(webapp2.RequestHandler):
    def render_template(self,filename,**template_args):
        path = os.path.join(os.path.dirname(__file__),'templates',filename)
        self.response.write(template.render(path,template_args))
    
class MainPage(BaseHandler):
    def get(self):
        self.render_template('base.html',name=self.request.get('name'))

class TransformPage(BaseHandler):
    def get(self):
        self.render_template('transform.html',name=self.request.get('form'))

    def post(self):
        field_storage = self.request.POST.get("coords",None)
        
        if isinstance(field_storage, cgi.FieldStorage):

            filename = field_storage.filename
            
            dyn = gcs_data.Dynamics(id=filename, filename=filename)
            gcs_filename = gcs_data.gcs_write_blob(dyn, field_storage.file.read())
            gcs_data.gcs_serving_url(dyn)
            dyn.put()
            logging.info('Transf: Uploaded and saved in default GCS bucket : ' + gcs_filename)
            ff_from = self.request.get('ff_from')
            ff_to = self.request.get('ff_to')
            email = self.request.get('email')
            
            # start transform as deferred tasks
            t = T(dyn,ff_from,ff_to,email)
            deferred.defer(t.run,dyn)
            self.redirect("/result?email="+email)
        else:
            self.redirect("/no_file_error")
            
class ConvertPage(BaseHandler):
    def get(self):
        self.render_template('convert.html',name=self.request.get('form'))

    def post(self):
        field_storage = self.request.POST.get("coords",None)
        
        if isinstance(field_storage,cgi.FieldStorage):
            
            filename = field_storage.filename
            
            dyn = gcs_data.Dynamics(id=filename,filename=filename)
            gcs_filename = gcs_data.gcs_write_blob(dyn, field_storage.file.read())
            gcs_data.gcs_serving_url(dyn)
            dyn.put()
            logging.info('Conv: Uploaded and saved in default GCS bucket : '+ gcs_filename)
            option_string = self.request.get('lin')
            lout = self.request.get('lout')
            email = self.request.get('email')
            n = self.request.get('n')

            # start deferred tasks
            c = C(dyn,option_string,lout,n,email)
            #_=deferred.defer(lipid_converter_convert,filename,option_string,lout,n,email)
            deferred.defer(c.run,dyn)
            self.redirect("/result?email="+email)
        else:
            self.redirect("/no_file_error")
            
class ResultPage(BaseHandler):
    def get(self):
        self.render_template('results.html',email=self.request.get('email'))
        
class HelpPage(BaseHandler):
    def get(self):
        self.render_template('help.html')

class ReferencesPage(BaseHandler):
    def get(self):
        self.render_template('references.html')

class NoFilePage(BaseHandler):
    def get(self):
        self.render_template('error_no_file.html')

class DownloadPage(BaseHandler):
    def get(self,file_id):
        self.render_template('download.html',file_id=file_id)
 
    def post(self):
        # is this safe here without any validation?              
        file_id = self.request.get('file_id')
        
        return self.redirect('/get?file_id='+file_id)
    
class GetPage(BaseHandler):
    def post(self,file_id):
        
        data = read_file(file_id)
        self.response.out.write(data)
        
        gro = re.compile('.gro')
        pdb = re.compile('.pdb')
        filetype = os.path.splitext(file_id)[1]
        
        if gro.match(filetype):
            t = 'binary/octet-stream'
        elif pdb.match(filetype):
            t = 'chemical/x-pdb'
        else:
            t = 'text/plain'
            
        encoding = 'utf-8'
                
        self.response.headers['Content-Type']=t
        self.response.headers['Content-Length'] = str(len(data))
        self.response.headers['Content-Disposition'] = 'attachment; filename=%s'%file_id
        
        return self.response


class ErrorPage(BaseHandler):
    def get(self):
        self.render_template('error.html')

class GetCodePage(BaseHandler):
    def get(self):
        self.render_template('get_code.html')
