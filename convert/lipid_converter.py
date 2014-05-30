#/usr/bin/env python
import sys
import os
import unicodedata
import re
import time
from hashlib import sha1
from random import randint

from structure import Protein
from transform import transform
from convert import convert
from storage import create_file,BUCKET

from google.appengine.api import mail
from google.appengine.ext import deferred

import gcs_data
import logging

def decode_incoming_options(option_string):
    options = re.compile(r'(.*)\.(.*)')
    tmp = re.findall(options,option_string)

    ffin = tmp[0][0]
    lin = tmp[0][1]

    return (ffin,lin)

def make_error_string_convert(ffin,lin,lout):
    e = "DEATH AND HORROR!!!\n\n"
    e = e + "No conversion between %s and %s in %s found\n"%(lin,lout,ffin)
    e = e + '\n\n'
    e = e + 'If your residue is called eg. POP and it is really POP(E,C,G,S), try renaming\n'
    e = e + 'Also make sure that your input file has the same atom nomenclature\n'
    e = e + 'as lipid-converter expects'
    return e

def make_error_string_transform(ffin,ffout,resname,resnum):
    e = "DEATH AND HORROR!!!\n\n"
    e = e + "No transformation from %s to %s for residue %s %d found\n"%(ffin,ffout,resname,resnum)
    e = e + '\n\n'
    e = e + 'If your residue is called eg. POP and it is really POP(E,C,G,S), try renaming\n'
    return e

def error_mail(response_string,email):
    
    mail.send_mail(sender='results@lipid-converter.appspotmail.com',
                   to=email,
                   subject='lipid-converter error',
                   body=response_string)


def response_mail(response_string,email):
    print response_string

    mail.send_mail(sender='results@lipid-converter.appspotmail.com',
                   to=email,
                   subject='lipid-converter results',
                   body=response_string)


def write(email,new_struct,filetype):

    rr = randint(0,1000)
    token = sha1(email)
    fn = token.hexdigest()+str(rr)+filetype
    
    gcs_file = create_file(BUCKET+fn)
    
    label = 'ATOM  '
    atalt = ' ' 
    chain = ' '
    resext = ' '
    occ = 1.0
    b = 0.0 
    elem = ''
    blank = ''

    formatted_out = ""

    for i in range(new_struct.atcounter):
        formatted_out = formatted_out + '%-6s%5d %4s%1s%-4s %4d   %8.3f%8.3f%8.3f%6.2f%6.2f          %2s%2s\n'%(label,i+1,new_struct.atname[i],atalt,new_struct.resname[i],new_struct.resnum[i],new_struct.coord[i][0]*10.,new_struct.coord[i][1]*10.,new_struct.coord[i][2]*10.,occ,b,blank,elem)
        
        if i%10==0:
            formatted_out = str(formatted_out)
            #print type(formatted_out)
            gcs_file.write(formatted_out)
            formatted_out = ""

    #formatted_out = formatted_out + '%10.5f%10.5f%10.5f'%(0,0,0)+'\n'
    gcs_file.write(formatted_out)
    gcs_file.close()
                           
    # Send mail from here for now                                              
    return fn

def finish(file_pieces,email,filetype):
    #print file_pieces
    data = []
    
    for i in range(len(file_pieces)):
        dyn = gcs_data.Dynamics(id=file_pieces[i],filename=file_pieces[i])
        tmp = gcs_data.gcs_read_blob(dyn)
        data.append(tmp)

    token = sha1(email)
    filename = token.hexdigest() + '_final_'+filetype
    dyn = gcs_data.Dynamics(id=filename,filename=filename)
    data_str = ''.join(data)
    gcs_filename = gcs_data.gcs_write_blob(dyn,data_str)
    gcs_data.gcs_serving_url(dyn)
    dyn.put()
    logging.info('Stored final file in default GCS bucket : '+gcs_filename)
    
    # Send mail from here for now                                           
    dn = 'lipid-converter.appspot.com/download/%s'%filename
    download_link = dn
    
    response_mail(download_link,email)
    
        
#def lipid_converter_transform(dyn,ffin,ffout,email):
    # Read in the input structure - pdb or gro based on file ending
    #print type(gcs_data.gcs_read_blob(dyn))
    #sys.exit()
#    struct = Protein(dyn,debug=0)

    # Decode from unicode to ascii
#    ffin = unicodedata.normalize('NFKD', ffin).encode('ascii','ignore')
#    ffout = unicodedata.normalize('NFKD', ffout).encode('ascii','ignore')
        
    # Do conversion or transformation
#    t = transform()
#    t.read_transforms()
#    new_struct = t.do(struct,ffin,ffout)
    
    # We always sort in the webapp
#    new_struct = new_struct.sort(ffout)    

    # And send away the results
#    prepare_result(new_struct,email)

#def lipid_converter_convert(filename,option_string,lout,n,email):
    # Read in the input structure - pdb or gro based on file ending
#    struct = Protein(filename,debug=0)
    
#    ffin,lin = decode_incoming_options(option_string)
    
    # Decode from unicode to ascii
#    lout = unicodedata.normalize('NFKD', lout).encode('ascii','ignore')
#    n = unicodedata.normalize('NFKD',n).encode('ascii','ignore')
#    ffin = unicodedata.normalize('NFKD',ffin).encode('ascii','ignore')
#    lin = unicodedata.normalize('NFKD',lin).encode('ascii','ignore')

#    n = int(n)
    
#    t = convert()
#    t.read_conversions()
#    new_struct = t.do(struct,ffin,lin,lout,n)
    
#    new_struct = new_struct.sort(ffin)    
#    prepare_result(new_struct,email)
    


class T():
    def __init__(self,dyn,ffin,ffout,email):
        self.ffin = ffin
        self.ffout = ffout
        self.email = email
        self.done_residues = 0
        self.file_pieces = []
        self.prot = None
        self.count = 0
        self.filetype = ""
        self.first_res = -1
        self.last_res = -1
        
    #def finish(self,email):

    #    print self.file_pieces
    #    data = []
    #    for i in range(len(self.file_pieces)):
    #        dyn = gcs_data.Dynamics(id=self.file_pieces[i],filename=self.file_pieces[i])
            #data = Protein(dyn)
    #        tmp = gcs_data.gcs_read_blob(dyn)
    #        data.append(tmp)
        
        
    #    token = sha1(email)
    #    filename = token.hexdigest() + '_final_'+self.filetype
    #    dyn = gcs_data.Dynamics(id=filename,filename=filename)
    #    data_str = ''.join(data)
    #    gcs_filename = gcs_data.gcs_write_blob(dyn,data_str)
    #    gcs_data.gcs_serving_url(dyn)
    #    dyn.put()
    #    logging.info('Stored final file in default GCS bucket : '+gcs_filename)
        
        # Send mail from here for now
    #    dn = 'lipid-converter.appspot.com/download/%s'%filename
    #    download_link = dn
        
    #    response_mail(download_link,email)    
    

    #def write(self,email,new_struct):
    #    rr = randint(0,1000)
    #    token = sha1(email)
    #    fn = token.hexdigest()+str(rr)+self.filetype
        
    #    gcs_file = create_file(BUCKET+fn)
        
    #    formatted_out = ""
    #    label = 'ATOM  '
    #    atalt = ' '
    #    chain = ' '
    #    resext = ' '
    #    occ = 1.0
    #    b = 0.0
    #    elem = ''
    #    blank = ''
        
    #    for i in range(new_struct.atcounter):
    #        formatted_out = formatted_out + '%-6s%5d %4s%1s%-4s %4d   %8.3f%8.3f%8.3f%6.2f%6.2f          %2s%2s\n'%(label,i+1,new_struct.atname[i],atalt,new_struct.resname[i],new_struct.resnum[i],new_struct.coord[i][0]*10.,new_struct.coord[i][1]*10.,new_struct.coord[i][2]*10.,occ,b,blank,elem)

     #       if i%10==0:
     #           gcs_file.write(formatted_out)
     #           formatted_out = ""

     #   gcs_file.write(formatted_out)
     #   gcs_file.close()
        
     #   self.file_pieces.append(fn)

    def run(self,dyn):
        new_struct = Protein()
        
        self.filetype = os.path.splitext(dyn.filename)[1]
        self.transform = transform()
        self.transform.read_transforms()
        
        # Get first residue number
        first_res = gcs_data.gcs_read_blob_get_first_resnum(dyn)
        self.first_res = first_res
        
        # Get the last residue number
        last_res = gcs_data.gcs_read_blob_get_last_resnum(dyn)
        self.last_res = last_res

        print "run: ffin=%s, ffout=%s, email=%s,first_res=%d"%(self.ffin,self.ffout,self.email,first_res)
        
        self._continue(dyn,first_res,new_struct)
        return
        
    def _continue(self,dyn,residue_start,new_struct):
        
        ffin = self.ffin
        ffout = self.ffout
        email = self.email

        # Total number of residues to process
        numres = self.last_res - self.first_res + 1
        # Do this many residues per task
        max_resnum_to_process = 100     
        
        self.prot = Protein(dyn,resstart=residue_start,resend=residue_start+max_resnum_to_process)
        #print "cbf: done_residues=%s, rumres=%d"%(self.done_residues,numres)
        
        # Have we done all the residues?
        if self.done_residues>=numres:
            #self.finish(email)
            finish(self.file_pieces,self.email,self.filetype)
            
        #print "START CONT"
        #new_struct.print_struct()
        #print "START CONT"
        
        #print self.prot.resnum
        #print self.prot.get_residues()
        #for resnum in self.prot.get_last_n_residues(self.done_residues):
        for resnum in self.prot.get_residues():
            residue = self.prot.get_residue_data(resnum)
            #print residue

            #print "c: resnum=%s,start=%d, done_residues=%d,count=%d"%(resnum,residue_start,self.done_residues,self.count)
            lipid = residue[0][1]
            
            # Find the proper transformation
            transf_atoms = self.transform.find_transformation(residue,ffin,ffout)
            if transf_atoms == -1:
                response_string = make_error_string_transform(ffin,ffout,lipid,resnum)
                error_mail(response_string,email)
                return
            
            try:
                hyd = self.transform.transforms[lipid,ffin,ffout]['hyd']
            except KeyError:
                hyd = ""
                
            # Do the transformation 
            transformed = self.transform.transform_residue(residue,transf_atoms)
            if hyd:
                transformed = self.transform.build_atoms(transformed,hyd)
                
            #print transformed
            # Add the result to a new protein
            new_struct.add_residue_data(transformed)
            #print "APA"
            #print new
            #print "APA DONE"
            #print transformed
            self.count = self.count + 1
            self.done_residues = self.done_residues + 1
            
            # Have we done all the residues?
            if self.done_residues>=numres:
                #print "DONE RESIDUES"
                # First, write the final part of the structure
                #self.write(email,new_struct)
                #del new_struct
                #new_struct.delete_all_residues()
                # Then do some magic to assemble results
                #self.finish(email)
                self.count = max_resnum_to_process
                self.done_residues = numres
                #return
                
            # If not,
            # check to prevent us from running over the time limit
            if self.count == max_resnum_to_process:
                #print "HERE"
                #self.write(new)
                #new_struct.print_struct()
                residue_start = resnum + 1
                self.count = 0
                #print "residue_start=%d"%residue_start
                #self.write(email,new_struct)
                fn = write(self.email,new_struct,self.filetype)
                self.file_pieces.append(fn)
                #del new_struct
                new_struct.delete_all_residues()
                deferred.defer(self._continue,dyn,residue_start,new_struct)
                return
        return



class C():
    def __init__(self,dyn,option_string,lout,n,email):
        
        ffin,lin = decode_incoming_options(option_string)
        
        self.ffin = str(ffin)
        self.ffout = str(ffin)
        self.lin = str(lin)
        self.lout = str(lout)

        self.email = str(email)
        self.done_residues = 0
        self.file_pieces = []
        self.prot = None
        self.count = 0
        self.n = int(n)
        self.filetype = ""
        self.first_res = -1
        self.last_res = -1
        self.convert_count = 0
        
    def run(self,dyn):
        new_struct = Protein()

        self.filetype = os.path.splitext(dyn.filename)[1]
        self.convert = convert()
        self.convert.read_conversions()
        
        first_res = gcs_data.gcs_read_blob_get_first_resnum(dyn)
        self.first_res = first_res
        
        last_res = gcs_data.gcs_read_blob_get_last_resnum(dyn)
        self.last_res = last_res

        print "c-run: ffin=%s,lin=%s,lout=%s,n=%s"%(self.ffin,self.lin,self.lout,self.n)
        print "c-run: first_res=%d, last_res=%d"%(self.first_res,self.last_res)
        
        self._continue(dyn,first_res,new_struct)
        return

    
    def _continue(self,dyn,residue_start,new_struct):
        
        ffin = self.ffin
        lin  = self.lin
        lout = self.lout
        n = self.n
        
        #Total number of resideus to process
        numres = self.last_res - self.first_res + 1
        # Do this many residues per task
        max_resnum_to_process = 100

        self.prot = Protein(dyn,resstart=residue_start,resend=residue_start+max_resnum_to_process)
        #print "c-cbf: done_residues=%s, numres=%d"%(self.done_residues,numres)
        
        # Have we done all the residues
        if self.done_residues >= numres:
            finish(self.file_pieces,self.email,self.filetype)
            
        #print self.prot.get_residues()
        for resnum in self.prot.get_residues():
            residue = self.prot.get_residue_data(resnum)
            resname = residue[0][1]

            transformed = []

            if resname == lin:
                self.convert_count = self.convert_count + 1
                                        
            if self.convert_count%n == 0 and resname==lin:
                try:
                    lipid = residue[0][1]
                    add_atoms = self.convert.conversions[ffin,lin,lout]['add']
                    rename_atoms = self.convert.conversions[ffin,lin,lout]['rename']
                    remove_atoms = self.convert.conversions[ffin,lin,lout]['remove']
                except:
                    response_string = make_error_string_convert(ffin,lin,lout)
                    error_mail(response_string,self.email)
                    return

                    # Do the conversions
                transformed = self.convert.remove_atoms(residue,remove_atoms)
                transformed = self.convert.rename_atoms(transformed,rename_atoms)
                transformed = self.convert.build_atoms(transformed,add_atoms)
                transformed = self.convert.update_resname(transformed,lout)
            else:
                transformed = residue
            
            # Add the (potentially converted) residue to a new protein
            new_struct.add_residue_data(transformed)
            
            self.count = self.count + 1
            self.done_residues = self.done_residues + 1

            # Have we done all the residues?
            if self.done_residues >= numres:
                self.count = max_resnum_to_process
                self.done_residues = numres
                
            # Do we need to start a new task?
            if self.count == max_resnum_to_process:
                residue_start = resnum + 1
                self.count = 0
                fn = write(self.email,new_struct,self.filetype)
                self.file_pieces.append(fn)
                new_struct.delete_all_residues()
                deferred.defer(self._continue,dyn,residue_start,new_struct)
                return
        return

                
