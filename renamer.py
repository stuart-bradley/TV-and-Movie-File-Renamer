"""
Batch renamer
Stuart Bradley
4/29/2014
"""

import os
import re
import shutil
import stat

loc = os.path.dirname(os.path.realpath(__file__)).replace("\\","/")

files_to_change = ['.avi', '.mp4', '.mkv', '.srt'] 

mode = ''

title = ''
date = ''
season_ep = ''

# Changes Season folder names based on dirnames.
def change_seasons(dirnames, root):
	for d in dirnames:
		# Season is correctly named.
		if re.search("Season \d{1,2}", d):
			continue
		# Find season num.
		matchObj = re.search("S(\d{1,2})|Season.(\d{1,2})", d)
		# Get first non-empty match and strip leading zeroes.
		season_num = next(s for s in matchObj.groups() if s).lstrip('0')
		os.rename(os.path.join(root, d).replace("\\","/"), os.path.join(root, "Season " + season_num).replace("\\","/"))

# Takes videos out of single folders, and places them in root directory.
def destroy_single_folders(dirnames, root):
	for d in dirnames:
		single_folder_root = os.path.join(root, d)
		for filename in os.listdir(single_folder_root):
			if filename.endswith(tuple(files_to_change)) and "sample" not in filename.lower():
				shutil.move(os.path.join(single_folder_root, filename), os.path.join(root, filename))
		shutil.rmtree(single_folder_root)

########
# MAIN #
########

for root, dirnames, filenames in os.walk(loc):
	# Set Root for WIN.
	root = root.replace("\\","/")
	# Determine main directory.
	if root.endswith("TV Shows"):
		mode = "TV"
	elif root.endswith("Movies"):
		mode = "Mo"

	if mode is "TV":
		# Check if in TV shows, and if inside a specific TV show. 
		matchObj = re.search("TV Shows\/([\w ]+$)",root)
		# Folder Structure.
		# Check if we're at Season level, and there are not files present.
		if not filenames and matchObj:
			# Set current Title.
			title = matchObj.group(1)
			# Set Season folder names.
			change_seasons(dirnames, root)
		# No video files, and Non-season directories visible, and directories contain S##E##.
		elif not any(x.endswith(tuple(files_to_change)) for x in filenames) and not any(re.search("Season \d+", x, re.IGNORECASE) for x in dirnames) and any(re.search("S\d+(?:E\d+)+", x, re.IGNORECASE) for x in dirnames):
			destroy_single_folders(dirnames, root)
		# If inside a season (video files are present).
		elif any(x.endswith(tuple(files_to_change)) for x in filenames):
			for f1 in filenames:
				# Video is correctly named.
				if re.search(" - S\d+(?:E\d+)+",f1):
					continue
				# Rename video, and subtitles.
				elif f1.endswith(tuple(files_to_change)):
					season_ep = re.search("([Ss]\d+[ ]*(?:[Ee]\d+)+)",f1).group(1).replace(" ", "").upper()
					ext = f1.split(".")[-1]
					os.rename(os.path.join(root, f1).replace("\\","/"), os.path.join(root, (title +  " - " + season_ep + "." +ext)).replace("\\","/"))
				# Trash.
				else:
					os.remove(os.path.join(root, f1).replace("\\","/"))	
	elif mode is "Mo":
		root = root.replace("\\","/")
		if any(x.endswith(tuple(files_to_change)) for x in filenames):
			title = re.search("Movies\/([\w\- ]+\(\d{4}\))",root).group(1)
			for f1 in filenames:
				# Video is correctly named.
				if re.search("[\w ]+\(\d{4}\).\w+",f1):
					continue
				# Rename video, and subtitles.
				elif f1.endswith(tuple(files_to_change)):
					ext = f1.split(".")[-1]
					os.rename(os.path.join(root, f1).replace("\\","/"), os.path.join(root, (title + "." +ext)).replace("\\","/"))
				# Trash.
				else:
					os.remove(os.path.join(root, f1).replace("\\","/"))
			print root
			main_root = re.search(r"(.+/)[^/]+$", root).group(1)
			os.rename(root, os.path.join(main_root, title).replace("\\","/"))