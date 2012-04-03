import re
import os

for entry in os.listdir('/home/taglio/Scrivania'):
    if re.match(".*"+search+".*" ,entry):
        print entry
		file_search.append(entry)

