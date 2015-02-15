count=0

import string;
def parseEmail( content ):
    content = content.strip();
    splt = content.split(".");
    str = "";
    for i in range(0,len(splt)):
        if bool(splt[i].strip()):
            str+="<s> "+splt[i].strip()+" </s>\n"
            'print(splt[i].strip())'
    return str;

DownspeakContent=''
UpspeakContent=''
with open('training.txt') as f:
	lines = f.readlines()
	currentEmail=""
	currentDownspeak=True
	for currentLine in lines:
		if currentLine=='DOWNSPEAK\n':
			currentDownspeak=True
		elif currentLine=='UPSPEAK\n':
			currentDownspeak=False		
		elif currentLine=='**START**\n':
			currentEmail=""
		elif currentLine=='**EOM**\n':
			parsedEmail=parseEmail(currentEmail))
			if currentDownspeak:
				DownspeakContent+=parsedEmail
			else:
				UpspeakContent+=parsedEmail
		else:
			currentEmail+=currentLine
			



	
