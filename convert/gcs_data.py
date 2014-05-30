#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, with_statement
 
from google.appengine.ext import blobstore
from google.appengine.api import app_identity, images
# to use cloudstorage include appengine-gcs-client-python-r127.zip in your project
import cloudstorage as gcs
from google.appengine.ext import ndb
import os
import mimetypes
# bonus, zip Dynamics entities and binary GCS blobs
import zipfile
import logging
import re 
 
class Dynamics(ndb.Model):
    filename = ndb.StringProperty()
    extension = ndb.ComputedProperty(lambda self: self.filename.rsplit('.', 1)[1].lower())
    serving_url = ndb.StringProperty(default=None)
 
#default_bucket = app_identity.get_default_gcs_bucket_name()
default_bucket = 'lipid-converter'
gae_development = os.environ['SERVER_SOFTWARE'].startswith('Development')
 
 
def gcs_serving_url(dyn):
    """ serving url for google cloud storage dyn entity """
 
    gcs_file_name = '/%s/%s' % (default_bucket, dyn.filename)
 
    if dyn.extension in ['png', 'jpg', 'gif']:
        dyn.serving_url = images.get_serving_url(
            blobstore.create_gs_key('/gs' + gcs_file_name), secure_url=True)
    elif gae_development:
        # this SDK feature has not been documented yet !!!
        dyn.serving_url = 'http://localhost:8080/_ah/gcs' + gcs_file_name    
    else:
        dyn.serving_url = 'https://storage.googleapis.com' + gcs_file_name
 
    return dyn.serving_url

def gcs_read_blob_get_last_resnum(dyn):
    gcs_file_name = '/%s/%s' % (default_bucket, dyn.filename)
    filetype = os.path.splitext(dyn.filename)[1]

    gro = re.compile('.gro')
    pdb = re.compile('.pdb')

    try:
        with gcs.open(gcs_file_name) as f:
            if gro.match(filetype):
                line = f.readline()
                line = f.readline()
                atcounter = int(line)
                
                for i in xrange(atcounter-1):
                    line = f.readline()
                    
                resi = int(line[0:5])
                return resi

            elif pdb.match(filetype):
                atom_hetatm = re.compile('(ATOM  |HETATM)')
                max_resi = -1
                line = f.readline()
                while line:
                    if atom_hetatm.match(line):
                        line = line[:-1]
                        resi = int(line[22:27])
                        if resi>max_resi:
                            max_resi = resi
                    line = f.readline()
                return resi
    
    except gcs.NotFoundError, e:
        logging.warning('GCS file %s NOT FOUND : %s' % (gcs_file_name, e))
        return None
                    
def gcs_read_blob_get_first_resnum(dyn):
    gcs_file_name = '/%s/%s' % (default_bucket, dyn.filename)
    filetype = os.path.splitext(dyn.filename)[1]

    gro = re.compile('.gro')
    pdb = re.compile('.pdb')
    
    try:
        with gcs.open(gcs_file_name) as f:
            if gro.match(filetype):
                line = f.readline()
                line = f.readline()
                line = f.readline()
                
                resi = int(line[0:5])
                return resi
            
            elif pdb.match(filetype):
                atom_hetatm = re.compile('(ATOM  |HETATM)')
                line = f.readline()
                while line:
                    if atom_hetatm.match(line):
                        line = line[:-1]
                        resi = int(line[22:27])
                        return resi
                    line = f.readline()
    except gcs.NotFoundError, e:
        logging.warning('GCS file %s NOT FOUND : %s' % (gcs_file_name, e))
        return None

def gcs_read_blob_resnum(dyn,resstart,resend):
    gcs_file_name = '/%s/%s' % (default_bucket, dyn.filename)
    filetype = os.path.splitext(dyn.filename)[1]
    
    gro = re.compile('.gro')
    pdb = re.compile('.pdb')
    
    data = []
    try:
        with gcs.open(gcs_file_name) as f:
            if gro.match(filetype):
                line = f.readline()
                line = f.readline()
                line = f.readline()
                while line:
                    # a gro-file has resnum here
                    #print line
                    try:
                        resi = int(line[0:5])
                        
                        if ( (resi >= resstart) and 
                             (resi<resend)):
                            data.append(line+'\n')
                    except ValueError:
                        pass
                    
                    line = f.readline()
                        
            elif pdb.match(filetype):
                atom_hetatm = re.compile('(ATOM  |HETATM)')
                line = f.readline()
                while line:
                    if atom_hetatm.match(line):
                        line = line[:-1]
                        
                        resi = int(line[22:27])
                        #print line,resi,resstart,resend
                        #print type(resi), type(resstart), type(resend)
                        #print resi,resstart,resend
                        if ( (resi >= resstart) and
                             (resi<resend)):
                            data.append(line+'\n')
                            #print line
                    line = f.readline() 
            else:
                print "Unknown filetype in gcs_data_read_resnum()"
                sys.exit()
    except gcs.NotFoundError, e:
        logging.warning('GCS file %s NOT FOUND : %s' % (gcs_file_name, e))
        return None
    
    #print data
    data_str = ''.join(data)
    return data_str

def gcs_read_blob(dyn):
    """ read binary blob from google cloud storage """

    gcs_file_name = '/%s/%s' % (default_bucket, dyn.filename)
    try:
        with gcs.open(gcs_file_name) as f:
            return f.read()
    except gcs.NotFoundError, e:
        logging.warning('GCS file %s NOT FOUND : %s' % (gcs_file_name, e))
        return None
 
 
def gcs_write_blob(dyn, blob):
    """ update google cloud storage dyn entity """
 
    gcs_file_name = '/%s/%s' % (default_bucket, dyn.filename)
    
    content_type = mimetypes.guess_type(dyn.filename)[0]
    if dyn.extension in ['js', 'css']:
        content_type += b'; charset=utf-8'
 
    with gcs.open(gcs_file_name, 'w', content_type=content_type,
                  options={b'x-goog-acl': b'public-read'}) as f:
        f.write(blob)
    
    return gcs_file_name

def gcs_content_type(dyn):

    gcs_file_name = '/%s/%s' % (default_bucket, dyn.filename)

    return gcs.stat(gcs_file_name).content_type


def gcs_zip_dynamics():
    """ bonus: save Dynamics and GCS blobs in a zip archive """
    
    gcs_file_name = '/%s/dynamics.zip' % default_bucket

    with gcs.open(gcs_file_name, 'w', content_type=b'multipart/x-zip') as f:

        with zipfile.ZipFile(f, 'w') as z:

            for each in Dynamics.query():
                member_dir = each.filename.replace('.', '_').encode('utf-8')
                z.writestr(b'%s/safe_key.txt' % member_dir, each.key.urlsafe().encode('utf-8'))
                z.writestr(b'%s/serving_url.txt' % member_dir, each.serving_url.encode('utf-8'))
                
                # if we have a GCS blob for this entity, save it in this member
                blob = gcs_read_blob(each)
                if blob:
                    z.writestr(b'%s/%s' % (member_dir, each.filename), blob)
                    z.writestr(b'%s/content_type.txt' % member_dir, gcs_content_type(each))


# example create a serving url
entity = Dynamics(id='test.pdf', filename='test.pdf')
gcs_serving_url(entity)
entity.put()
