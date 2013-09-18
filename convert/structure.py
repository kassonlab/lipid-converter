import math
import re
import os
import sys
import numpy as np
from forcefields import ff_sortings
from storage import *

import cloudstorage as gcs

Vsites = ['MN1','MN2']
directive = re.compile('^ *\[ *(.*) *\]')

class Sort:
    def __init__(self):
        self.sorts = {}

    def sort(self,ff):
        # Get everything
        self.read_sortings()

        new = Protein()
        
        for resnum in self.get_residues():
            residue = self.get_residue_data(resnum)
            out = self.sort_residue(residue,ff)
            new.add_residue_data(out)

        return new
        
    def sort_residue(self,residue,ff):

        # Get the name of the residue to be sorted
        resname = residue[0][1]
        #print residue[0]
        sort_data = self.sorts[ff,resname]['atoms']

        out = [0]*len(sort_data)
        #print sort_data
        for i,ai in enumerate(sort_data):
            ai = sort_data[i][0]
            
            for j in range(len(residue)):
                aj = residue[j][0]
                
                if ai == aj:
                    #print ai,aj
                    out[i]=(aj,
                            residue[j][1],
                            residue[j][2],
                            residue[j][3])
        #print out
        return out
                
    def read_sortings(self):
        for ff in ff_sortings:
            fn = ""
            
            try:
                path = os.path.dirname(__file__)
                path = os.path.join(path,ff,'sortings.top')
                fn = open(path,'r')
            except:
                print "Could not open sortings file for %s"%ff

            atoms = []
            lipid = ""
            
            for line in fn:
                s = line.strip()
                
                if s.startswith("["):
                    d = re.findall(directive,s)[0].strip().lower()

                    # If we get to end of an entry, store it 
                    if d=='end':

                        # Create a new dict for this entry 
                        m = {}
                        m['atoms']=atoms
                        #print ff,lipid
                        self.sorts[ff,lipid]=m
                        # Reset atoms  
                        atoms = []
                        
                    continue
                if not s:
                    continue
                
                elif d == 'atoms':
                    atoms.append(s.split())

                elif d == 'molecule':
                    lipid = s.split()[0]


class Protein(Sort):
    def __init__(self,file_in=None,debug=0):
        self.title=''
        self.atcounter = 0
        
        self.header = []
        self.footer = []
        
        self.label = []
        self.atnum = []
        self.elem = []
        self.mass = []
        self.atname = []
        self.atalt = []
        self.resname = []
        self.chain = []
        self.resnum = []
        self.resext = []
        self.coord = []
        self.occ = []
        self.b = []
        self.sequence = {}
        self.box = []
        self.velocity = []
        
        self.debug = debug
        
        # Read in the file based on its extension
        if file_in:
            filetype = os.path.splitext(file_in)[1]
            
            gro = re.compile('.gro')
            pdb = re.compile('.pdb')
            
            f = BUCKET + file_in
            gcs_file = gcs.open(f,'r')
            data = gcs_file.read()
            #print data
            #print "DATA"
            if gro.match(filetype):
                self.read_gro(data)
            elif pdb.match(filetype):
                self.read_pdb(data)
            else:
                print "Unknown file-type"
                sys.exit()
                
        # We also need to inititate the Sort base class here
        # This is a bit weird, but I'm a noob at oop anyway :-)
        Sort.__init__(self)

    def read_pdb(self,data,debug=0):
        #lines = file(file_in).readlines()
        lines = data
        self.read_pdb_lines(lines,debug)
        
    def read_pdb_lines(self,lines,debug):
        i = 0
        atom_hetatm = re.compile('(ATOM  |HETATM)')
        #head = re.compile('^(HEADER|COMPND|REMARK|SEQRES|CRYST1|SCALE|ORIG)')
        #title = re.compile('^TITLE')
        #foot = re.compile('(CONECT |TER  |MASTER|END)')
        #element = re.compile('[A-Za-z ][A-Za-z]')
        for line in lines:
            if atom_hetatm.match(line):
                line = line[:-1]
                #self.label.append(line[0:6])
                #self.atnum.append(int(line[6:12]))
                self.atname.append(line[12:16].strip())
                #self.atalt.append(line[16:17])
                self.resname.append(line[17:21].strip())
                #self.chain.append(line[21])
                self.resnum.append(int(line[22:26]))
                #self.resext.append(line[27])
                self.coord.append((float(line[30:38])/10, float(line[38:46])/10, float(line[46:54])/10))
                #self.occ.append(float(line[54:60]))
                #self.b.append(float(line[60:66]))
                #self.velocity.append(0.0)
                #if element.match(line[76:78]):
                #    self.elem.append(line[76:78])
                #else:
                #    self.elem.append(line[12:14])
                    
                self.atcounter += 1
                
                i = i + 1
            
            #elif head.match(line):
            #    self.header.append(line[:-1])
            #elif foot.match(line):
            #    self.footer.append(line[:-1])
            #elif title.match(line):
            #    self.title = self.title + line[10:-1].strip() + " "

        if debug:
            return len(self.atnum),self.atcounter
                            
    def read_gro(self,data,debug=0):
        #lines = file(file_in).readlines()
        lines = data.split('\n')
        #print lines
        self.read_gro_lines(lines,debug)
        
    def read_gro_lines(self,lines,debug):
        #print lines[0]
        #print lines[1]
        #print "FOO"
        self.title = lines[0][:-1]
        self.atcounter = int(lines[1])
        #print "HEJ"
        #print lines[1]
        #print lines[1][:-1]
        #print "HOPP"
        if self.debug:
            print self.title
            print self.atcounter
            print lines[2][:-1],len(lines[2])
        
        #print len(lines)
        #print self.atcounter
        #print "FFFFFFFFFFFFFFFFFFFFFFFFFFFF"
        for line in lines[2:self.atcounter+3][:-1]:
            self.resnum.append(int(line[0:5]))
            self.resname.append(line[5:10].strip())
            self.atname.append(line[10:15].strip())
            self.atnum.append(int(line[15:20]))

            first_decimal = line.index('.')
            second_decimal = line[first_decimal+1:].index('.')
            incr = second_decimal + 1
            self.coord.append((float(line[20:20+incr]), float(line[28:20+2*incr]), float(line[36:20+3*incr])))
            #print line
            # are there velocities
            #if len(line) == 68:
            #    self.velocity.append((float(line[44:20+4*incr])*10., float(line[52:5*incr])*10., float(line[60:6*incr])*10.))
            #else:
            #    self.velocity.append((0.0,0.0,0.0))
    
    def get_residues(self):
        res = np.unique(self.resnum)
        return res

    # Return data for residue resi
    def get_residue_data(self,resi):
        out = []
        
        for i in range(self.atcounter):
            if self.resnum[i]==resi:
                
                out.append((#self.atnum[i],
                            self.atname[i],
                            #self.atalt[i],
                            self.resname[i],
                            #self.chain[i],
                            self.resnum[i],
                            #self.resext[i],
                            self.coord[i]))
                            #self.occ[i],
                            #self.b[i]))
                
        return out
                
    def add_residue_data(self,residue):
        
        for i in range(len(residue)):
            atname = residue[i][0]
            resname = residue[i][1]
            resnum = residue[i][2]
            coords = residue[i][3]

            self.resnum.append(resnum)
            self.resname.append(resname)
            self.atname.append(atname)
            self.coord.append(coords)

            self.atcounter = self.atcounter + 1
            
    def write_pdb(self,file_out):
        f = open(file_out,'w')

        for i in range(self.atcounter):
            self.write_pdb_line(f,i)

        f.close()

    def write_pdb_line(self,file_out,i):
        label = 'ATOM  '
        atalt = ' '
        chain = ' '
        resext = ' '
        occ = 1.0
        b = 0.0
        elem = ''
        blank = ''

        # This isn't the strict pdb format string, but it lets us
        # write pdb-files that have 4-letter long reside codes
        # and 5-numbered residue numbers
        file_out.write('%-6s%5d %-4s%1s%4s %4d   %8.3f%8.3f%8.3f%6.2f%6.2f          %2s%2s\n'%(label,i+1,self.atname[i],atalt,self.resname[i],self.resnum[i],self.coord[i][0]*10.,self.coord[i][1]*10.,self.coord[i][2]*10.,occ,b,blank,elem)) 
        
    def write_gro(self,file_out):
        f = open(file_out,'w')
        
        f.write('lipid-converter gro-file\n')
        f.write('%d\n'%self.atcounter)

        for i in range(self.atcounter):
            self.write_gro_line(f,i)

        f.write('%10.5f%10.5f%10.5f'%(0,0,0))
        f.close()

    def write_gro_line(self,file_out,i):
        file_out.write("%5d%-5s%5s%5d%8.3f%8.3f%8.3f\n"%(self.resnum[i]%1e5,self.resname[i],self.atname[i],i+1,self.coord[i][0],self.coord[i][1],self.coord[i][2]))

    def write(self,filename):
        filetype = os.path.splitext(filename)[1]
        
        gro = re.compile('.gro')
        pdb = re.compile('.pdb')
        
        if gro.match(filetype):
            self.write_gro(filename)
        elif pdb.match(filetype):
            self.write_pdb(filename)
        else:
            print "Unknown filetype in write"
            sys.exit()


