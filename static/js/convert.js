function setOptions(chosen,selbox){
    
    selbox.options.length = 0;
    
    if (chosen == " ") {
	selbox.options[selbox.options.length] = new Option('Select a force field first',' ');
	setTimeout(setOptions(' ',document.trans.lout),5);
    }
    if (chosen == "charmm36") {
	selbox.options[selbox.options.length] = new Option('POPC','charmm36.POPC');
	selbox.options[selbox.options.length] = new Option('POPE','charmm36.POPE');
	selbox.options[selbox.options.length] = new Option('POPG','charmm36.POPG');
	selbox.options[selbox.options.length] = new Option('POPS','charmm36.POPS');
	selbox.options[selbox.options.length] = new Option('DOPC','charmm36.DOPC');
	selbox.options[selbox.options.length] = new Option('DMPC','charmm36.DMPC');
	selbox.options[selbox.options.length] = new Option('DPPC','charmm36.DPPC');
	setTimeout(setOptions('charmm36.POPC',document.trans.lout),5);
    }
    if (chosen == "gromos43a1-S3") {
	selbox.options[selbox.options.length] = new Option('POPC','gromos43a1-S3.POPC');
	selbox.options[selbox.options.length] = new Option('POPE','gromos43a1-S3.POPE');
	selbox.options[selbox.options.length] = new Option('DMPC','gromos43a1-S3.DMPC');
	selbox.options[selbox.options.length] = new Option('DOPC','gromos43a1-S3.DOPC');
	selbox.options[selbox.options.length] = new Option('DPPC','gromos43a1-S3.DPPC');
	selbox.options[selbox.options.length] = new Option('DLPC','gromos43a1-S3.DLPC');
	setTimeout(setOptions('gromos43a1-S3.POPC',document.trans.lout),5);
    }
    
    // Finally we present the choices for output lipid based on what is implemented
    if (chosen == "charmm36.POPC") {
	// this is charmm36 and from POPC ->
	selbox.options[selbox.options.length] = new Option('POPG','POPG');
	selbox.options[selbox.options.length] = new Option('POPE','POPE');
	selbox.options[selbox.options.length] = new Option('POPS','POPS');
	selbox.options[selbox.options.length] = new Option('DOPC','DOPC');
	selbox.options[selbox.options.length] = new Option('DMPC','DMPC');
	selbox.options[selbox.options.length] = new Option('DPPC','DPPC');
    }
    if (chosen == "charmm36.POPE") {
	// this is charmm36 and from POPE ->
	selbox.options[selbox.options.length] = new Option('POPC','POPC');
	selbox.options[selbox.options.length] = new Option('POPG','POPG');
	selbox.options[selbox.options.length] = new Option('POPS','POPS');
	selbox.options[selbox.options.length] = new Option('DOPC','DOPC');
	selbox.options[selbox.options.length] = new Option('DMPC','DMPC');
	selbox.options[selbox.options.length] = new Option('DPPC','DPPC');	
    }
    if (chosen == "charmm36.POPG") {
	// this is charmm36 and from POPG ->
	selbox.options[selbox.options.length] = new Option('POPC','POPC');
	selbox.options[selbox.options.length] = new Option('POPE','POPE');
	selbox.options[selbox.options.length] = new Option('POPS','POPS');
	selbox.options[selbox.options.length] = new Option('DOPC','DOPC');
	selbox.options[selbox.options.length] = new Option('DMPC','DMPC');
	selbox.options[selbox.options.length] = new Option('DPPC','DPPC');	
    }
    if (chosen == "charmm36.POPS") {
	// this is charmm36 and from POPS ->
	selbox.options[selbox.options.length] = new Option('POPC','POPC');
	selbox.options[selbox.options.length] = new Option('POPE','POPE');
	selbox.options[selbox.options.length] = new Option('POPG','POPG');
	selbox.options[selbox.options.length] = new Option('DOPC','DOPC');
	selbox.options[selbox.options.length] = new Option('DMPC','DMPC');
	selbox.options[selbox.options.length] = new Option('DPPC','DPPC');	
    }
    if (chosen == "charmm36.DOPC") {
	// this is charmm36 and from DOPC ->
	selbox.options[selbox.options.length] = new Option('POPC','POPC');
	selbox.options[selbox.options.length] = new Option('POPE','POPE');
	selbox.options[selbox.options.length] = new Option('POPG','POPG');
	selbox.options[selbox.options.length] = new Option('POPS','POPS');
	selbox.options[selbox.options.length] = new Option('DMPC','DMPC');
	selbox.options[selbox.options.length] = new Option('DPPC','DPPC');	
    }
    if (chosen == "charmm36.DMPC") {
	// this is charmm36 and from DMPC ->
	selbox.options[selbox.options.length] = new Option('POPC','POPC');
	selbox.options[selbox.options.length] = new Option('POPE','POPE');
	selbox.options[selbox.options.length] = new Option('POPG','POPG');
	selbox.options[selbox.options.length] = new Option('POPS','POPS');
	selbox.options[selbox.options.length] = new Option('DOPC','DOPC');
	selbox.options[selbox.options.length] = new Option('DPPC','DPPC');	
    }
    if (chosen == "charmm36.DPPC") {
	// this is charmm36 and from DPPC ->
	selbox.options[selbox.options.length] = new Option('POPC','POPC');
	selbox.options[selbox.options.length] = new Option('POPE','POPE');
	selbox.options[selbox.options.length] = new Option('POPG','POPG');
	selbox.options[selbox.options.length] = new Option('POPS','POPS');
	selbox.options[selbox.options.length] = new Option('DOPC','DOPC');
	selbox.options[selbox.options.length] = new Option('DMPC','DMPC');	
    }
    if (chosen == "gromos43a1-S3.POPC") {
	// this is gromos43a1-S3 and from POPC
	selbox.options[selbox.options.length] = new Option('POPE','POPE');
	selbox.options[selbox.options.length] = new Option('DMPC','DMPC');
	selbox.options[selbox.options.length] = new Option('DOPC','DOPC');
	selbox.options[selbox.options.length] = new Option('DPPC','DPPC');
	selbox.options[selbox.options.length] = new Option('DLPC','DLPC');
    }
    if (chosen == "gromos43a1-S3.POPE") {
	// this is gromos43a1-S3 and from POPE
	selbox.options[selbox.options.length] = new Option('POPC','POPC');
	selbox.options[selbox.options.length] = new Option('DMPC','DMPC');
	selbox.options[selbox.options.length] = new Option('DOPC','DOPC');
	selbox.options[selbox.options.length] = new Option('DPPC','DPPC');
	selbox.options[selbox.options.length] = new Option('DLPC','DLPC');
    }
    if (chosen == "gromos43a1-S3.DMPC") {
	// this is gromos43a1-S3 and from DMPC
	selbox.options[selbox.options.length] = new Option('POPC','POPC');
	selbox.options[selbox.options.length] = new Option('POPE','POPE');
	selbox.options[selbox.options.length] = new Option('DOPC','DOPC');
	selbox.options[selbox.options.length] = new Option('DPPC','DPPC');
	selbox.options[selbox.options.length] = new Option('DLPC','DLPC');
    }
    if (chosen == "gromos43a1-S3.DOPC") {
	// this is gromos43a1-S3 and from DOPC
	selbox.options[selbox.options.length] = new Option('POPC','POPC');
	selbox.options[selbox.options.length] = new Option('POPE','POPE');
	selbox.options[selbox.options.length] = new Option('DMPC','DMPC');
	selbox.options[selbox.options.length] = new Option('DPPC','DPPC');
	selbox.options[selbox.options.length] = new Option('DLPC','DLPC');
    }
    if (chosen == "gromos43a1-S3.DPPC") {
	// this is gromos43a1-S3 and from DPPC
	selbox.options[selbox.options.length] = new Option('POPC','POPC');
	selbox.options[selbox.options.length] = new Option('POPE','POPE');
	selbox.options[selbox.options.length] = new Option('DMPC','DMPC');
	selbox.options[selbox.options.length] = new Option('DOPC','DOPC');
	selbox.options[selbox.options.length] = new Option('DLPC','DLPC');
    }
    if (chosen == "gromos43a1-S3.DLPC") {
	// this is gromos43a1-S3 and from DLPC
	selbox.options[selbox.options.length] = new Option('POPC','POPC');
	selbox.options[selbox.options.length] = new Option('POPE','POPE');
	selbox.options[selbox.options.length] = new Option('DMPC','DMPC');
	selbox.options[selbox.options.length] = new Option('DOPC','DOPC');
	selbox.options[selbox.options.length] = new Option('DPPC','DPPC');
    }
}
	
    
