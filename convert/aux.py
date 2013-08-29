import math
import numpy as np

distH = 0.1
alphaH = np.arccos(-1/3.0)
s6 = 0.5 * np.sqrt(3.0)

def setup(xAI,xAJ,xAK):
    rij = 0.0
    ra = 0.0
    
    sij = []
    sb = []
    sa = []
    
    for i in range(3):
        xd = xAJ[i]
        sij.append(xAI[i]-xd)
        sb.append(xd-xAK[i])
        rij+=np.square(sij[i])
        
    rij = np.sqrt(rij)
    
    sa.append(sij[1]*sb[2]-sij[2]*sb[1])
    sa.append(sij[2]*sb[0]-sij[0]*sb[2])
    sa.append(sij[0]*sb[1]-sij[1]*sb[0])
    
    for i in range(3):
        sij[i]=sij[i]/rij
        ra+=np.square(sa[i])
        
    ra = np.sqrt(ra)

    for i in range(3):
        sa[i]=sa[i]/ra
        
    sb.append(sa[1]*sij[2]-sa[2]*sij[1])
    sb.append(sa[2]*sij[0]-sa[0]*sij[2])
    sb.append(sa[0]*sij[1]-sa[1]*sij[0])
    
    return sa,sb,sij

def one_single_atom(xAI,xAJ,xAK):
    
    xH1 = []
    sa,sb,sij = setup(xAI,xAJ,xAK)
    
    for i in range(3):
        xH1.append(xAI[i]+distH*np.sin(alphaH)*sb[i]-distH*np.cos(alphaH)*sij[i])
        
    return xH1

def two_atoms(xAI,xAJ,xAK):
    r1 = []
    r2 = []
    r2 = []
    
    xH1 = []
    xH2 = []
    
    for i in range(3):
        r1.append(xAI[i]-0.5*(xAJ[i]+xAK[i]))
        
    b = np.linalg.norm(r1)
    r2 = np.subtract(xAI,xAJ)
    r3 = np.subtract(xAI,xAK)
    r4 = np.cross(r2,r3)
    n  = np.linalg.norm(r4)
    
    for i in range(3):
        xH1.append(xAI[i]+distH*(np.cos(alphaH/2.0*r1[i]/b+np.sin(alphaH/2.0)*r4[i]/n)))
        xH2.append(xAI[i]+distH*(np.cos(alphaH/2.0*r1[i]/b-np.sin(alphaH/2.0)*r4[i]/n)))
        
    return xH1, xH2

def three_atoms(xAI,xAJ,xAK):
    xH1 = []
    xH2 = []
    xH3 = []
    
    sa,sb,sij = setup(xAI,xAJ,xAK)
    
    for i in range(3):
        xH1.append(xAI[i]+distH*np.sin(alphaH)*sb[i]-distH*np.cos(alphaH)*sij[i])
        
        xH2.append(xAI[i]-
                   distH*np.sin(alphaH)*0.5*sb[i] +
                   distH*np.sin(alphaH)*s6*sa[i] -
                   distH*np.cos(alphaH)*sij[i])
        
        xH3.append(xAI[i]-
                   distH*np.sin(alphaH)*0.5*sb[i] -
                   distH*np.sin(alphaH)*s6*sa[i] -
                   distH*np.cos(alphaH)*sij[i])
        
    return xH1,xH2,xH3

# Compare two lists of atoms    
def check_atoms(target_atoms,atoms):
    s = list(set(target_atoms)-set(atoms))
    s1 = list(set(atoms)-set(target_atoms))
    
    return s,s1


# Return the residue name for atom ai in list l                                
def get_resn(l,ai):
    resn = ""
    
    for i in range(len(l)):
        try:
            if l[i] and l[i][0].strip()==ai:
                resn = l[i][1]
        except:
            print "Error in get_resn(): ai=%s",ai
            sys.exit()
            
    return resn
        
def get_resi(l,ai):
    resi = -1
    
    for i in range(len(l)):
        try:
            if l[i] and l[i][0].strip()==ai:
                resi = l[i][2]
        except:
            print "Error in get_resi(): ai=%s",ai
            sys.exit()

    return resi

def get_chain(l,ai):
    chain = ""
    
    for i in range(len(l)):
        try:
            if l[i] and l[i][0].strip()==ai:
                chain = l[i][3]
        except:
            print "Error in get_chain(): ai=%s"%ai
            sys.exit()
            
    return chain


# Return the position in list for atom ai in list l                            
def get_pos_in_list(l,ai):
    
    pos = -1
    
    for i in range(len(l)):
        try:
            if l[i] and l[i][0].strip()==ai:
                pos = i
        except TypeError:
            print "Error in get_pos_in_list(): ai=%s"%ai
            sys.exit()

    return pos

# Return the xyz coordinates of the atom in ai in list l                       
def get_xyz_coords(l,ai):
    
    xyz = np.zeros((3,))
    
    for i in range(len(l)):
        try:
            if l[i] and l[i][0].strip()==ai:
                xyz[0]=l[i][4]
                xyz[1]=l[i][5]
                xyz[2]=l[i][6]
        except TypeError:
            print "Error in get_xyz_coords(): ai=%s"%ai
            sys.exit()
            
    return xyz
