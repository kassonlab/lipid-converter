#/usr/bin/env python
import sys
import os
import gflags
from structure import Protein
from transform import transform
from convert import convert

# Use gflags to get command line options
FLAGS = gflags.FLAGS

gflags.DEFINE_string('mode','transform',
                     'Do transformation or conversion')

gflags.DEFINE_string('f','conf.pdb',
                     'Input pdb structure')
gflags.DEFINE_string('o','out.pdb',
                     'Output pdb structure')

gflags.DEFINE_string('ffin', 'berger',
                     'source force field')
gflags.DEFINE_string('ffout', 'charmm36',
                     'target force field')

gflags.DEFINE_string('lin', 'POPC',
                     'input lipid')
gflags.DEFINE_string('lout', 'POPG',
                     'output lipid')
gflags.DEFINE_integer('n', 1,
                      'Convert every n-th lipid')

gflags.DEFINE_bool('canonical',False,
                   'Turn on canonical sorting')
gflags.DEFINE_bool('longresnum',False,
                   'Assume 5-digit residue numbers in pdb-files')

argv = FLAGS(sys.argv)

# Read in the input structure - pdb or gro based on file ending
struct = Protein(FLAGS.f,FLAGS.longresnum,debug=0)

# Do conversion or transformation
if FLAGS.mode == 'transform':
    t = transform()
    t.read_transforms()
    new_struct = t.do(struct,FLAGS.ffin,FLAGS.ffout)
elif FLAGS.mode == 'convert':
    t = convert()
    t.read_conversions()
    new_struct = t.do(struct,FLAGS.ffin,FLAGS.lin,FLAGS.lout,FLAGS.n)
else:
    print "Either transform or convert please...!"
    sys.exit()

# Does it make sense to sort here?
if FLAGS.canonical:

    # If we are changing from one forcefield to another, we are
    # sorting according to the output ff
    if FLAGS.mode == 'transform':
        ff_sort = FLAGS.ffout
    
    # And similarily, if we are changing a lipid type within a forcefield,
    # we sort on this ff (ie the input ff)
    if FLAGS.mode == 'convert':
        ff_sort = FLAGS.ffin
        
    # We also need a special trick for amber/lipids11, since the residue
    # names are identical between different lipids (the plug-and-play
    # architecture differentiates between different lipid headgroups and
    # tails, so that different lipids with the same tails will have the same
    # residue names.
    # We therefore loop over the input structure and save an array with the
    # old residue names
    # Todo: work out something when going from an amber/lipid11 coordinate
    # file (probably some kind of third file with residue names)
    resmap = None    
    if ff_sort == 'lipid11':
        resmap = struct.get_resnames()
        
    new_struct = new_struct.sort(ff_sort,resmap)    

# Write out result
new_struct.write(FLAGS.o)
