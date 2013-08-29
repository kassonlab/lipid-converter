import sys,os,glob,re
import sys,inspect
from collections import defaultdict

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import aux

class ConvertMap:
    def __init__(self,rename=None,add=None,remove=None,natoms=-1,lipid_to=""):
        
        self.add = add
        self.remove = remove
        self.rename = rename
        self.natoms = int(natoms)

        self.lipid_to = lipid_to

    def convert(self,residue):
        
        # These are the atoms we have
        atoms = [i[0].strip() for i in residue]

        # Remove atoms
        if self.remove:
            for i in range(len(self.remove)):
                for j,a1 in enumerate(atoms):
                    if a1 == self.remove[i][0]:
                        pos = aux.get_pos_in_list(residue,a1)
                        residue.pop(pos)
                                                

        # Then rename
        if self.rename:
            for i in range(len(self.rename)):
                at_from,at_to = self.rename[i]
                
                for j,a1 in enumerate(atoms):
                    if a1 == at_from:
                        pos = aux.get_pos_in_list(residue,a1)
                        
                        residue[pos] = (at_to,
                                        self.lipid_to,
                                        residue[j][2],
                                        residue[j][3],
                                        residue[j][4],
                                        residue[j][5],
                                        residue[j][6])


        # Finally add missing atoms
        if self.add:
            for i in range(len(self.add)):

                h,suffix,ai,aj,ak = self.add[i]

                xAI = aux.get_xyz_coords(residue,ai)
                xAJ = aux.get_xyz_coords(residue,aj)
                xAK = aux.get_xyz_coords(residue,ak)
                
                resn = self.lipid_to
                resi = aux.get_resi(residue,ai)
                chain = aux.get_chain(residue,ai)
                pos = aux.get_pos_in_list(residue,ai)

                num = len(suffix)
                
                if num==1:
                    x1 = aux.one_single_atom(xAI,xAJ,xAK)
                    name = h
                    residue.insert(pos+1,(name,resn,resi,chain,x1[0],x1[1],x1[2]))
                    
                elif num==2:
                    x1,x2 = aux.two_atoms(xAI,xAJ,xAK)
                    name1 = h + suffix[0]
                    name2 = h + suffix[1]
                    residue.insert(pos+1,(name1,resn,resi,chain,x1[0],x1[1],x1[2]))
                    residue.insert(pos+2,(name2,resn,resi,chain,x2[0],x2[1],x2[2]))
                elif num==3:
                    x1,x2,x3 = aux.three_atoms(xAI,xAJ,xAK)
                    name1 = h + suffix[0]
                    name2 = h + suffix[1]
                    name3 = h + suffix[2]
                    residue.insert(pos+1,(name1,resn,resi,chain,x1[0],x1[1],x1[2]))
                    residue.insert(pos+2,(name2,resn,resi,chain,x2[0],x2[1],x2[2]))
                    residue.insert(pos+3,(name3,resn,resi,chain,x3[0],x3[1],x3[2]))
                else:
                    print "Need to specify either 1,2 or 3 atoms around the central atom"
                    print "Currently it is %d"%num
                    print "Bailing out..."
                    sys.exit()


        # We should now have a residues array of length self.natoms
        atoms = [i[0].strip() for i in residue]
        
        #print atoms
        #print len(atoms)
        #print self.natoms

        if not len(residue)==self.natoms:
            print "Something is wrong in converting..."
            sys.exit()

        # Set all residue names to the new residue
        residue = [list(i) for i in residue]
        for i in range(self.natoms):
            residue[i][1]=self.lipid_to
        
        return residue

def _init():
    mapping = {}
    source = ""
    ff = ""
    target = ""
    natoms = -1
    rename = []
    add = []
    remove = []
    directive = re.compile('^ *\[ *(.*) *\]')
    
    for fn in glob.glob(os.path.dirname(__file__)+'/*map'):
        for line in open(fn):
            s = line.strip()

            if s.startswith("["):
                cur = re.findall(directive,s)[0].strip().lower()

                if cur == 'end':
                    try:
                        mapping[(ff,source,target)]=ConvertMap(rename=rename,
                                                               add=add,
                                                               remove=remove,
                                                               natoms=natoms,
                                                               lipid_to=target)
                    except:
                        print "Could not read conversion between %s and %s for forcefield %"%(source,target,ff)
                    
                    rename,add,remove = [],[],[]
                continue

            s = s.split(";")[0].strip()

            if not s:
                continue
            
            elif cur == 'molecule':
                source = s.split()[0]

            elif cur == 'forcefield':
                ff = s.split()[0]

            elif cur == 'target':
                target = s.split()[0]

            elif cur == 'rename':
                rename.append(s.split())

            elif cur == 'add':
                add.append(s.split())

            elif cur == 'remove':
                remove.append(s.split())

            elif cur == 'natoms':
                natoms = s.split()[0]

    return mapping
                

convert = _init()

ff = 'charmm36'

final_map = defaultdict(dict)

def get(lipid_from,lipid_to):
    # Create a dictionary for this forcefield and lipid mapping only,
    # like so final_map['POPC']['POPG']
    for i in convert.keys():
        if i[0]==ff and i[1]==lipid_from and i[2]==lipid_to:
            final_map[i[1]][i[2]]=convert[i]
            
    return final_map
