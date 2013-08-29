import glob
import os

class Sorting:
    def __init__(self,atoms=None):
        self.atoms = atoms

    def sort(self,residue):
        print residue
        
        print self.atoms
        print len(self.atoms)

        transformed = [0]*len(self.atoms)
        
        atoms = [i[0].strip() for i in residue ]

        for i in range(len(self.atoms)):
            a1 = self.atoms[i]

            for j,a2 in enumerate(atoms):
                if a1 == a2:
                    transformed[i]=(a2,
                                    residue[j][1],
                                    residue[j][2],
                                    residue[j][3],
                                    residue[j][4],
                                    residue[j][5],
                                    residue[j][6])
        return transformed

def _init():

    sorting = {}

    for fn in glob.glob(os.path.dirname(__file__)+'/*sort'):
        
        ff = os.path.basename(fn).split('.')[0]
        lipid = os.path.basename(fn).split('.')[1].upper()
        atoms = []
        
        for line in open(fn):
            s = line.strip()
            atoms.extend(s.split())
            
            sorting[(ff,lipid)]=Sorting(atoms=atoms)
            
    return sorting

sorting = _init()

def get(ff):
    final_map = dict([(i[1],sorting[i]) for i in sorting.keys() if i[0]==ff])
    return final_map
