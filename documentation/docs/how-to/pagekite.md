#Pagekite

Pagekite is a python script that will allow your computer to be accessed from the internet from an address such as http://ke8crv.pagekite.me


##ODroid (or Raspberry PI)

###SSH Keys
Make sure you have exchanged ssh keys with the geonode server.

ssh-keygen
ssh-copy-id -i odroid@<geonode server ip>

You should be able to ssh into the geonode server without a password

###DTMF Tones 
Run sdr_to_multimon_dtmf.sh

This will cause the DTMF tones to be collected using rtl_fm, demodulated using multimon-ng, and analyzed using Python.

This will be the command issued when the correct DTMF tone is heard

odroid@<geonode server ip> 'python /home/odroid/pagekite.py'


I used a python script to generate DTMF tones and also recorded my call sign into a wav file for testing purposes.