import os
import glob
import re
from structure import Protein
from forcefields import ff_conversions
import aux

import sys

directive = re.compile('^ *\[ *(.*) *\]')

class convert():
    def __init__(self):
        self.conversions = {}
        
    def read_conversions(self):
        for ff in ff_conversions:
            fn = ""

            try:
                path = os.path.dirname(__file__)
                path = os.path.join(path,ff,'conversions.top')
                fn = open(path,'r')
            except:
                print "Could not open convert file for %s"%ff
                
            add_atoms = []
            remove = []
            rename = []
            
            lin = ""
            lout = ""

            for line in fn:
                s = line.strip()
                
                if s.startswith("["):
                    d = re.findall(directive,s)[0].strip().lower()
                    
                    # If we get to end of an entry, store it
                    if d=='end':
                        
                        # Create a new dict for this entry
                        m = {}
                        m['add']=add_atoms
                        m['remove']=remove
                        m['rename']=rename
                        #print m
                        #print remove
                        # Add this combination of ff,lin and lout
                        # as a tuple key
                        self.conversions[ff,lin,lout]=m
                        
                        # Reset these three
                        rename = []
                        add_atoms = []
                        remove = []

                    continue

                if not s:
                    continue

                elif d == 'rename':
                    rename.append(s.split())
                    
                elif d == 'add':
                    add_atoms.append(s.split())
                    
                elif d == 'remove':
                    remove.append(s.split())

                elif d == 'molecule':
                    lin = s.split()[0]

                elif d =='target':
                    lout = s.split()[0]

    def do(self,prot,ff,lin,lout,n):

        new = Protein()
        #print self.transforms['POPC','berger','charmm36']
        #sys.exit()
        for resnum in prot.get_residues():
            if resnum%n==0:
                
                residue = prot.get_residue_data(resnum)

                try:
                    lipid = residue[0][1]
                    add_atoms = self.conversions[ff,lin,lout]['add']
                    rename_atoms = self.conversions[ff,lin,lout]['rename']
                    remove_atoms = self.conversions[ff,lin,lout]['remove']
                except:
                    print "No conversion between %s and %s in %s found"%(lin,lout,ff)
                    sys.exit()

            # Do the conversions
                transformed = self.remove_atoms(residue,remove_atoms)
            #new.add_residue_data(transformed)
            #new.write('test.pdb')
            #sys.exit()
                transformed = self.rename_atoms(transformed,rename_atoms)
            #new.add_residue_data(transformed)
            #new.write('test.pdb')
            #sys.exit()
                transformed = self.build_atoms(transformed,add_atoms)
            #new.add_residue_data(transformed)
            #new.write('test.pdb')
            #sys.exit()
                transformed = self.update_resname(transformed,lout)
                            #print transformed
                            #
            #sys.exit()
            #print hyd
            #sys.exit()
            
            #print transformed
            #sys.exit()
            # Add the result to a new protein
                new.add_residue_data(transformed)
            #new.write('test.pdb')
            #print new.atname
            #print new.coord
            #sys.exit()
        return new
            
    def remove_atoms(self,residue,remove_atoms):
        
        # Make a local copy of the atom names her
        # so we can make operations on the residue 
        # list in the loop
        atoms = [i[0].strip() for i in residue]

        for i in range(len(remove_atoms)):
            ai = remove_atoms[i][0]
            
            for j in range(len(atoms)):
                aj = atoms[j]
                #print ai,aj
                if ai == aj:
                    
                    # This is important since atoms and residue
                    # will be out of sync 
                    pos = aux.get_pos_in_list(residue,aj)
                    residue.pop(pos)
                    
        #print residue
        #sys.exit()
        return residue


    def rename_atoms(self,residue,rename_atoms):
        for i in range(len(rename_atoms)):
            ai = rename_atoms[i][0]
            aout = rename_atoms[i][1]

            for j in range(len(residue)):
                aj = residue[j][0]
                
                if ai == aj:
                    #print ai,aout
                    residue[j]=(aout,
                                residue[j][1],
                                residue[j][2],
                                residue[j][3])
        return residue
                    
    def build_atoms(self,residue,add_atoms):
        #print add_atoms
        for i in range(len(add_atoms)):
            
            # Get the data for building atoms
            name,suffix,ai,aj,ak = add_atoms[i]
            #print name,suffix,ai,aj,ak
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
        

    def update_resname(self,residue,lout):
        residue = [list(i) for i in residue]
        
        for i in range(len(residue)):
            residue[i][1]=lout
    
        return residue
