import webapp2
from handlers import *

application = webapp2.WSGIApplication([
        ('/',MainPage),
        ('/convert',ConvertPage),
        ('/result',ResultPage),
        ('/transform',TransformPage),
        ('/help',HelpPage),
        ('/references',ReferencesPage),
        ('/download/(.*)',DownloadPage),
        ('/get/(.*)',GetPage),
        ('/error',ErrorPage),
        ('/source',GetCodePage),
        ('/no_file_error',NoFilePage),
        ],debug=True)
                                      

