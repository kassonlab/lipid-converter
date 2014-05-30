function setOptions(chosen){
    
    var selbox = document.convert.ff_to;
    selbox.options.length = 0;
    
    if (chosen == " ") {
	selbox.options[selbox.options.length] = new Option('Select an input force field',' ');
    }
    if (chosen == "charmm36") {
	// charmm36
	selbox.options[selbox.options.length] = new Option('Berger','berger');
	selbox.options[selbox.options.length] = new Option('Gromos43A1-S3','gromos43a1-S3');
	selbox.options[selbox.options.length] = new Option('Gromos53A6','gromos53a6');
	selbox.options[selbox.options.length] = new Option('Gromos54A7','gromos54a7');
	selbox.options[selbox.options.length] = new Option('OPLS-UA','opls');
    }
    if (chosen == "berger") {
	// Berger
	selbox.options[selbox.options.length] = new Option('Charmm36','charmm36');
	selbox.options[selbox.options.length] = new Option('Gromos43A1-S3','gromos43a1-S3');
    }
    if (chosen == "gromos43a1-S3") {
	// gromos43a1S3
	selbox.options[selbox.options.length] = new Option('Charmm36','charmm36');
	selbox.options[selbox.options.length] = new Option('Berger','berger');
    }
    if (chosen == "gromos53a6") {
	// gromos53a6
	selbox.options[selbox.options.length] = new Option('Charmm36','charmm36');
    }
    if (chosen == "gromos54a7") {
	// gromos54a7
	selbox.options[selbox.options.length] = new Option('Charmm36','charmm36');
    }
    if (chosen == "opls") {
	// gromos54a7
	selbox.options[selbox.options.length] = new Option('Charmm36','charmm36');
    }
}

    
