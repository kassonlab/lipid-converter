#/usr/bin/env python
import sys
import os
import unicodedata
from hashlib import sha1

from structure import Protein
from transform import transform
from convert import convert
from storage import create_file,BUCKET

from google.appengine.api import mail

def response_mail(response_string,email):
    print response_string

    mail.send_mail(sender='results@lipid-converter.appspot.com',
                   to=email,
                   subject='lipid-converter results',
                   body=response_string)


def prepare_result(new_struct,ffin,ffout,email):
    
    label = 'ATOM  '
    atalt = ' ' 
    chain = ' '
    resext = ' '
    occ = 1.0
    b = 0.0 
    elem = ''
    blank = ''

    # Start to save result
    token = sha1(email)
    gcs_file = create_file(BUCKET+token.hexdigest())

    formatted_out = ""
    #formatted_out = formatted_out + 'Transformed from %s to %s\n'%(ffin,ffout)
    #formatted_out = formatted_out + '%5d\n'%(new_struct.atcounter)

    for i in range(new_struct.atcounter):
        formatted_out = formatted_out + '%-6s%5d %-4s%1s%4s %4d   %8.3f%8.3f%8.3f%6.2f%6.2f          %2s%2s\n'%(label,i+1,new_struct.atname[i],atalt,new_struct.resname[i],new_struct.resnum[i],new_struct.coord[i][0]*10.,new_struct.coord[i][1]*10.,new_struct.coord[i][2]*10.,occ,b,blank,elem)
        
        if i%10==0:
            gcs_file.write(formatted_out)
            formatted_out = ""

    #formatted_out = formatted_out + '%10.5f%10.5f%10.5f'%(0,0,0)+'\n'
    gcs_file.write(formatted_out)
    gcs_file.close()
                           
    # Send mail from here for now                                              
    dn = 'lipid-converter.appspot.com/download/%s'%token.hexdigest()
    download_link = dn

    response_mail(download_link,email)

        
def lipid_converter_transform(filename,ffin,ffout,email):
    # Read in the input structure - pdb or gro based on file ending
    struct = Protein(filename,debug=0)
    
    # Decode from unicode to ascii
    ffin = unicodedata.normalize('NFKD', ffin).encode('ascii','ignore')
    ffout = unicodedata.normalize('NFKD', ffout).encode('ascii','ignore')
    
    # Do conversion or transformation
    t = transform()
    t.read_transforms()
    new_struct = t.do(struct,ffin,ffout)
    
    # We always sort in the webapp
    new_struct = new_struct.sort(ffout)    

    # And send away the results
    prepare_result(new_struct,ffin,ffout,email)

def lipid_converter_convert(filename,ffin,lin,lout,n,email):
    t = convert()
    t.read_conversions()
    new_struct = t.do(struct,ffin,lin,lout,n)
    
    new_struct = new_struct.sort(ffin)    
    
# Does it make sense to sort here?

