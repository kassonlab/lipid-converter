import os
import glob
import re
from structure import Protein
from forcefields import ff_transformations
import aux

import sys
import sets

directive = re.compile('^ *\[ *(.*) *\]')

class transform():
    def __init__(self):
        self.transforms = {}
        
    def read_transforms(self):
        for ff in ff_transformations:
            
            fn = ""

            try:
                path = os.path.dirname(__file__)
                path = os.path.join(path,ff,'transforms.top')
                fn = open(path,'r')
            except:
                print "Could not open transform file for %s"%ff
            
            transf = []
            transf2 = []
            hyd = []
            ffout = ""
            lipid = ""

            for line in fn:
                s = line.strip()
                
                if s.startswith("["):
                    d = re.findall(directive,s)[0].strip().lower()
                    
                    # If we get to end of an entry, store it
                    if d=='end':
                        
                        # Create a new dict for this entry
                        m = {}
                        m['transf']=transf
                        m['transf2']=transf2
                        if hyd:
                            m['hyd']=hyd
                        
                            # Add this combination of lipid, ff and ffout
                            # as a tuple key
                        self.transforms[lipid,ff,ffout]=m
                        
                        # Reset these two
                        transf = []
                        transf2 = []
                        hyd = []

                    continue

                if not s:
                    continue

                elif d == 'atoms':
                    transf.append(s.split())
                    
                elif d == 'atoms2':
                    transf2.append(s.split())

                elif d == 'hydrogens':
                    hyd.append(s.split())

                elif d == 'molecule':
                    lipid = s.split()[0]

                elif d =='target':
                    ffout = s.split()[0]

    #def do(self,prot,ffin,ffout):

    #    new = Protein()
        #print self.transforms['POPC','berger','charmm36']
        #sys.exit()
    #    for resnum in prot.get_residues():
    #        residue = prot.get_residue_data(resnum)
            #print "BAJS"
            #print residue
            #print "APA"
    #        try:
    #            lipid = residue[0][1]
    #            transf_atoms = self.transforms[lipid,ffin,ffout]['transf']
    #            try:
    #                hyd = self.transforms[lipid,ffin,ffout]['hyd']
    #            except KeyError:
    #                hyd = ""
    #        except:
    #            print "No transformation from %s to %s for residue %s %d found"%(ffin,ffout,lipid,resnum)
    #            sys.exit()

            # Do the transformation
    #        transformed = self.transform_residue(residue,transf_atoms)
            #print transformed
            #new.add_residue_data(transformed)
            #new.write('test.pdb')
            #sys.exit()
            #print hyd
            #sys.exit()
    #        if hyd:
    #            transformed = self.build_atoms(transformed,hyd)
            
            #print transformed
            #sys.exit()
            # Add the result to a new protein
    #        new.add_residue_data(transformed)
            #new.write('test.pdb')
            #print new.atname
            #print new.coord
            #sys.exit()
    #    del prot
    #    return new
    
    def find_transformation(self,residue,ffin,ffout):
        
        # Read in the transformations for this residue
        lipid = residue[0][1]
        
        try:
            transf = self.transforms[lipid,ffin,ffout]['transf']
        except:
            print "transform.py: No primary transformation from %s to %s for residue %s found"%(ffin,ffout,lipid)
            return -1
        
        try:
            transf2 = self.transforms[lipid,ffin,ffout]['transf2']
        except:
            # As long as the primary transformation was found, this is ok
            pass

        # Now see if we match any of these, start with making a list of atom
        # names
        atnames = []
        for i in range(len(residue)):
            atnames.append(residue[i][0])

        # And make lists of the atoms in the transforms
        atn1 = []
        for i in range(len(transf)):
            atn1.append(transf[i][0])
            
        # If we are adding more transforms, this gets a bit cumbersome in that
        # we need to have tranfs3 etc, but I'm to tired to put this in a loop
        if transf2:
            atn2 = []
            for i in range(len(transf2)):
                atn2.append(transf2[i][0])
        
        # Start to compare
        s_atnames = sets.Set(atnames)
        satn1 = sets.Set(atn1)
        
        if transf2:
            satn2 = sets.Set(atn2)
            if satn2 == s_atnames:
                return transf2
            
        if satn1 == s_atnames:
            return tranfs
        else:
            return -1
        
        
    def transform_residue(self,residue,transf_atoms):
        out = []
        #print transf_atoms
        for i in range(len(residue)):
            ain = residue[i][0]
            
            for j in range(len(transf_atoms)):
                #print ain,transf_atoms[j][1]
                if ain == transf_atoms[j][0]:
                    aout = transf_atoms[j][1]
                    
                    resn = residue[i][1]
                    resi = residue[i][2]
                    coords = residue[i][3]

                    out.append((aout,resn,resi,coords))
                    #print ain,aout,i,j
                    break
        #print out
        #sys.exit()
        return out

    def build_atoms(self,residue,hyd):
        
        for i in range(len(hyd)):
            
            # Get the data for building atoms
            name,suffix,ai,aj,ak = hyd[i]
            
            # Number of atoms to build is based on the length of the
            # suffix string
            num = len(suffix)
            
            xai = aux.get_xyz_coords(residue,ai)
            xaj = aux.get_xyz_coords(residue,aj)
            xak = aux.get_xyz_coords(residue,ak)

            pos   = aux.get_pos_in_list(residue,ai)
            resn  = aux.get_resn(residue,ai)
            resi  = aux.get_resi(residue,ai)

            if num==1:
                x1 = aux.one_single_atom(xai,xaj,xak)
                x1_name = name
                residue.insert(pos+1,(x1_name,resn,resi,(x1[0],x1[1],x1[2])))

            elif num==2:
                x1,x2 = aux.two_atoms(xai,xaj,xak)
                x1_name = name+suffix[0]
                x2_name = name+suffix[1]
                residue.insert(pos+1,(x1_name,resn,resi,(x1[0],x1[1],x1[2])))
                residue.insert(pos+2,(x2_name,resn,resi,(x2[0],x2[1],x2[2])))

            elif num==3:
                x1,x2,x3 = aux.three_atoms(xai,xaj,xak)
                x1_name = name+suffix[0]
                x2_name = name+suffix[1]
                x3_name = name+suffix[2]
                residue.insert(pos+1,(x1_name,resn,resi,(x1[0],x1[1],x1[2])))
                residue.insert(pos+2,(x2_name,resn,resi,(x2[0],x2[1],x2[2])))
                residue.insert(pos+2,(x3_name,resn,resi,(x3[0],x3[1],x3[2])))
            else:
                print "Need to specify either 1,2 or 3 hydrogens to construct around central atom %s"%ai
                print "Currently it is %d"%num
                print "Bailing out..."
                
                sys.exit()
        #print residue
        return residue
        

    
    
