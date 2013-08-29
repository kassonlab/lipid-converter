import math

d2r = math.pi/180.0

# Names of vites that are discarded when reading. 
# Make this into a file instead
Vsites = ['MN1','MN2']

class Structure:
    def __init__(self,other,strict=False):

        if type(other) == str:
            lines = open(other).readlines()
        else:
            lines = other

            
        # Extract PDB atom/hematms and set the box
        self.box = None
        rest = []

        self.atoms = [self.pdbAtom(i,strict) for i in lines if self.isPDBAtom(i,Vsites) or rest.append(i)]
        
        # If no atoms where found, this was a gro-file
        if not self.atoms:
            n = int(lines[1])+2
            self.atoms = [self.groAtom(i) for i in lines[2:n] if self.isGROAtom(i,Vsites)]
            b = [float(i) for i in lines[n].split()] + 6*[0]
            self.box = [[b[0],b[3],b[4]],[b[5],b[1],b[6]],[b[7],b[8],b[2]]] 
        else:
            b = [i for i in rest if i.startswith("CRYST1")]
            if b:
                self.box = self.pdbBoxRead(b[-1])
                

        # Build a residue list
        self.residues = [[self.atoms[0]]]
        for i in self.atoms[1:]:
            if i[1:4] != self.residues[-1][-1][1:4]:
                self.residues.append([])
            self.residues[-1].append(i)        


        # Extract the sequence    
        self.sequence = [ i[0][1].strip() for i in self.residues ]

    def isPDBAtom(self,l,Vsites):
        if l.startswith("ATOM") or l.startswith("HETATM"):
            
            # Discard any vsites while reading
            atname = l[12:16].strip()
            if not atname in Vsites:
                return l 

        
    def pdbAtom(self,a,strict=False):
        if strict:
            return (str(a[12:16]),str(a[17:20]),int(a[22:26]),a[21],float(a[30:38])/10,float(a[38:46])/10,float(a[46:54])/10)
        else:
            return (str(a[12:16]),str(a[17:21]),int(a[22:26]),a[21],float(a[30:38])/10,float(a[38:46])/10,float(a[46:54])/10)
        
        
    def isGROAtom(self,a,Vsites):
        atname = a[10:15].strip()
        if not atname in Vsites:
            return a
            
    def groAtom(self,a):
        return (str(a[10:15]), str(a[5:10]),   int(a[:5]), " ", float(a[20:28]),float(a[28:36]),float(a[36:44]))


    def pdbBoxRead(self,a):
        fa, fb, fc, aa, ab, ac = [float(i) for i in a.split()[1:7]]
        ca, cb, cg, sg         = math.cos(d2r*aa), math.cos(d2r*ab), math.cos(d2r*ac) , math.sin(d2r*ac)
        wx, wy                 = 0.1*fc*cb, 0.1*fc*(ca-cb*cg)/sg
        wz                     = math.sqrt(0.01*fc*fc - wx*wx - wy*wy)
        return [[0.1*fa, 0, 0], [0.1*fb*cg, 0.1*fb*sg, 0], [wx, wy, wz]]
    
    def groBox(self):
        groBox = "%10.5f%10.5f%10.5f"
        
        if self.box:
            return groBox % (self.box[0][0],self.box[1][1],self.box[2][2])
        else:
            return groBox % (0,0,0)
