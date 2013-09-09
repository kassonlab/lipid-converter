import sys
import unicodedata
from hashlib import sha1

from google.appengine.api import mail
import cloudstorage as gcs

import Mapping
import Convert
import Sorting
from structure import Structure
from storage import *

def finish():
    return 0

def response_mail(response_string,email):

    print response_string

    mail.send_mail(sender='per.larsson@sbc.su.se',
                   to=email,
                   subject='lipid-conversion-results',
                   body=response_string)
    

def lipid_converter(filename,ff_from,ff_to,email):
    
    # read in this file
    filename = BUCKET + filename
    gcs_file = gcs.open(filename,'r')
    data = gcs_file.read().split('\n')
        
    struct = Structure(data)
    
    mapping = Mapping.get(ff_from=ff_from,ff_to=ff_to)
    sorting = Sorting.get(ff=ff_to)
    
    out = []

    for residue in struct.residues:
        # Unpack to get the residue name
        _,resn,resi,_,_,_,_ = residue[0]
        resn = resn.strip()
        
        # Do the transformation 
        if resn in mapping.keys():
            res = mapping[resn].convert(residue)
            res = sorting[resn].sort(res)
            out.extend(res)
        else:
            error = "No mapping between %s and %s for residue %s %d was found\n"%(ff_from,ff_to,resn,resi)
            error = error + "Maybe you need to rename from %s to POP{C|E|S|G}\n"%resn
            response_mail(error,email)
            return 0

    formatted_out = ""
    formatted_out = formatted_out + 'Transformed from %s to %s\n'%(ff_from,ff_to)
    formatted_out = formatted_out + '%5d\n'%len(out)
    
    count = 1
    for atom in out:
        at,resn,resi,chain,x,y,z = atom
        formatted_out = formatted_out + "%5d%-5s%5s%5d%8.3f%8.3f%8.3f\n"%(resi%1e5,resn,at,count%1e5,x,y,z)
        count = count + 1

    formatted_out = formatted_out + struct.groBox()+'\n'
    
    # For some reason we need to decode from unicode to ascii here
    # Is this safe to do?
    formatted_out = unicodedata.normalize('NFKD', formatted_out).encode('ascii','ignore')
    
    token = sha1(email)
    save_to_cloud(formatted_out,token.hexdigest())
    
    # Send mail from here for now
    dn = 'lipid-converter.appspot.com/download/%s'%token.hexdigest()
    download_link = dn

    response_mail(download_link,email)
    #print token.hexdigest()
    
