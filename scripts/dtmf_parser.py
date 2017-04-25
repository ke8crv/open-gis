import sys, re

'''
dtmf_parser - this builds a dtmf passcode and 

TODO
Create a subprocess that runs pagekite
If this script closes, make sure the subprocess closes

OR

insert a status into the database and create a separate
script on the remote server that queries the database for timestamp
 and runs cron job that checks status and launches pagekite
'''

dtmf_pattern = re.compile("^([0-9\#\*A-D,a-d]{1})$")


def checkDTMF(dtmf):
	print "Checking:" + dtmf
	passcode = "112358"
	if dtmf == passcode:
		print "Valid passcode"
	else:
		print "Invalid passcode"	
	return

def main():

	
	print "DTMF Testing"
	char_array = []
	
	while(True):
		tone_char = sys.stdin.readline()
		tone_char = tone_char.strip()
		tone_char = tone_char.replace("DTMF: ","")
	
		if len("".join(char_array)) >= 15:
			print "Too many characters"
			checkDTMF("".join(char_array))
			char_array = []

		elif "#" in tone_char:
			checkDTMF( "".join(char_array))
			char_array = []

		else:	
			if dtmf_pattern.match(tone_char):
				char_array.append(tone_char)
			else:
				print "Invalid character"


if __name__ == "__main__":

	main()
