from django import forms

choices_from = (
    ('berger','Berger'),
    ('charmm36','Charmm36')
)

choices_to = (
    ('charmm36','Charmm36'),
)

class ConvertForm(forms.Form):    

    ff_from = forms.ChoiceField(choices=choices_from,
                                label='Source FF:')
    ff_to = forms.ChoiceField(choices=choices_to,
                              label='Target FF:')
    email = forms.EmailField(label='Email address for result:',
                             required=False)
    pdb = forms.FileField(label='Upload file to convert',
                          required=True)
        
