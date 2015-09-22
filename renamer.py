"""
Batch renamer
Stuart Bradley
4/29/2014
"""

import os
import glob
import re

files_to_change = '*.avi' 

for f in glob.glob(files_to_change):
		if re.search('S\d+E\d+', f):
			print 'Already in S##E## format - Skipping'
			continue
		else:
			titleArray = f.split()
			season = titleArray[6]
			episode = titleArray[8]
			f2 = 'Two And A Half Men - S' + season + 'E' + episode + '.avi'
        	print 'renaming: ', f, ' -> ', f2
        	os.rename(f, f2) 
print 'All Done' 
 
 
