import os,sys,re,glob,inspect
import numpy as np

# Inelegant solution to be able to import modules from the parent
# directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
                
import aux
                
class AtomMap:
    def __init__(self,atoms=None,hyd=None,natoms=-1):

        self.hyd = ""
        
        if atoms:
            x  = [i[0] for i in atoms]
            y  = [i[1] for i in atoms]

        assert len(x) == len(y)
        
        self.target_atoms = x
        self.source_atoms = y
        self.hyd = hyd
        self.natoms = int(natoms)
        
    def convert(self,residue):
        # Given a residue, return the corresponding residue with
        # names changed to the new force field nomenclature
                # Also, if necessary, build hydrogen atoms according 
        # to specification in .map-file
               
        # These are the atoms we have in the input file
        atoms = [ i[0].strip() for i in residue]

        # These are the atoms we need in to have the input file
        source_atoms = self.source_atoms

        # These are the atoms we are transforming into
        target_atoms = self.target_atoms
        
        # First, check that we got all the atoms we expect
        s,s1 = aux.check_atoms(source_atoms,atoms)
        
        if len(s)>0 or len(s1)>0:
            print "Residue %s %s"%(residue[0][1],residue[0][2])
            print "Expected:"
            print s
            print "Found:"
            print s1
            sys.exit()
            
        transformed = []
        
        # Do the conversion
        # We loop over atoms here rather than source_atoms (they contain
        # the same atoms at this stage, but atoms have them in the order of the input
        # file
            
        for i,a1 in enumerate(atoms):

            a2 = target_atoms[i]
            
            resn = residue[i][1]
            resi = residue[i][2]
            chain = residue[i][3]
            x = residue[i][4]
            y = residue[i][5]
            z = residue[i][6]
            
            transformed.append((a2,resn,resi,chain,x,y,z))

        #print transformed
        # Add in the hydrogens, if specified in the map file
        if self.hyd:
            for i in range(len(self.hyd)):
                
                # Unpack the hydrogen line
                h,suffix,ai,aj,ak = self.hyd[i]
                num = len(suffix)
                
                # Get coordinates of the constructing atoms
                xAI   = aux.get_xyz_coords(transformed,ai)
                xAJ   = aux.get_xyz_coords(transformed,aj)
                xAK   = aux.get_xyz_coords(transformed,ak)
                
                pos   = aux.get_pos_in_list(transformed,ai)

                resn  = aux.get_resn(transformed,ai)
                resi  = aux.get_resi(transformed,ai)
                chain = aux.get_chain(transformed,ai)
                
                if num==1:
                    xH1 = aux.one_single_atom(xAI,xAJ,xAK)
                    xH1_name = h
                    transformed.insert(pos+1,(xH1_name,resn,resi,chain,xH1[0],xH1[1],xH1[2]))
                
                elif num==2:
                    xH1,xH2 = aux.two_atoms(xAI,xAJ,xAK)
                    xH1_name = h+suffix[0]
                    xH2_name = h+suffix[1]
                    
                    transformed.insert(pos+1,(xH1_name,resn,resi,chain,xH1[0],xH1[1],xH1[2]))
                    transformed.insert(pos+2,(xH2_name,resn,resi,chain,xH2[0],xH2[1],xH2[2]))
                    
                elif num==3:
                    xH1,xH2,xH3 = aux.three_atoms(xAI,xAJ,xAK)
                    xH1_name = h+suffix[0]
                    xH2_name = h+suffix[1]
                    xH3_name = h+suffix[2]
                    
                    transformed.insert(pos+1,(xH1_name,resn,resi,chain,xH1[0],xH1[1],xH1[2]))
                    transformed.insert(pos+2,(xH2_name,resn,resi,chain,xH2[0],xH2[1],xH2[2]))
                    transformed.insert(pos+3,(xH3_name,resn,resi,chain,xH3[0],xH3[1],xH3[2]))
                else:
                    print "Need to specify either 1,2 or 3 hydrogens to construct around central atom %s"%ai
                    print "Currently it is %d"%num
                    print "Bailing out..."
                
                    sys.exit()
                
        print transformed
        return transformed
    

def _init():

    mapping = {}
    mol = ""
    natoms = -1
    aa = []
    hydrogens = []
    ff_from = ""
    ff_to = ""
    directive = re.compile('^ *\[ *(.*) *\]')

    for fn in glob.glob(os.path.dirname(__file__)+"/*map2"):

        for line in open(fn):
            
            s = line.strip()
            
            # Check for directive
            if s.startswith("["):
                
                # Extract the directive name
                cur = re.findall(directive,s)[0].strip().lower()
                
                # When at the end of a conversion file, add the translation table to the mapping dictionary
                if cur == 'end':
                    try:
                        mapping[(mol,ff_from,ff_to)] = AtomMap(atoms=aa,hyd=hydrogens,natoms=natoms)
                    except:
                        print "Could not read mapping between %s and %s for residue %s"%(ff_from,ff_to,mol)

                    # and empty the atoms and hydrogen lists
                    aa,hydrogens = [],[]
                    
                continue
            
            # Remove comments
            s = s.split(";")[0].strip()
            
            if not s:
                continue
            
            elif cur == "molecule":
                mol = s.split()[0]
            
            elif cur == "source":
                ff_from = s.split()[0]
                
            elif cur == "target":
                ff_to = s.split()[0]
                
            elif cur == "atoms":
                aa.append(s.split())
                
            elif cur == "hydrogens":
                hydrogens.append(s.split())
         
            elif cur == "natoms":
                natoms = s.split()[0]

    return mapping

    
mapping = _init()

def get(ff_from,ff_to):
    final_map = dict([(i[0],mapping[i]) for i in mapping.keys() if i[1]==ff_from and i[2]==ff_to])
    print final_map.keys()
    return final_map
