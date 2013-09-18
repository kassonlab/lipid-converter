import os
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.ext import deferred
from storage import *
from lipid_converter import lipid_converter_transform

class BaseHandler(webapp2.RequestHandler):
    def render_template(self,filename,**template_args):
        path = os.path.join(os.path.dirname(__file__),'templates',filename)
        self.response.write(template.render(path,template_args))
    
class MainPage(BaseHandler):
    def get(self):
        self.render_template('base.html',name=self.request.get('name'))

class ConvertPage(BaseHandler):
    def get(self):
        self.render_template('convert.html',name=self.request.get('form'))

    def post(self):
        filename = self.request.POST['coords'].filename
        filesize = int(self.request.headers['Content_Length'])
        
        if filesize>5242880:
            self.redirect('/error')
        else:
            save_to_cloud(self.request.get('coords'),filename)
            
            ff_from = self.request.get('ff_from')
            ff_to = self.request.get('ff_to')
            email = self.request.get('email')
            
            # start deferred tasks
            _=deferred.defer(lipid_converter_transform,filename,ff_from,ff_to,email)
            
            self.redirect("/result?email="+email)
        
class ResultPage(BaseHandler):
    def get(self):
        self.render_template('results.html',email=self.request.get('email'))
        
class TransformPage(BaseHandler):
    def get(self):
        self.render_template('transform.html')

class HelpPage(BaseHandler):
    def get(self):
        self.render_template('help.html')

class ReferencesPage(BaseHandler):
    def get(self):
        self.render_template('references.html')

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
        
        t = 'text/plain'
        encoding = 'utf-8'
                
        self.response.headers['Content-Type']=t
        self.response.headers['Content-Length'] = str(len(data))
        self.response.headers['Content-Disposition'] = 'attachment; filename=results.gro'
        
        return self.response


class ErrorPage(BaseHandler):
    def get(self):
        self.render_template('error.html')
