#-*- encoding: utf8 -*-

"""
The purpose of this file is to store some common Python functions
that we can use everywhere inside the code..

Author: Alper KANAT  <alperkanat@raptiye.org>
"""

def summarize(text, limit=0):
	"""
	Removes all HTML tags and cuts the text by limit
	
	text (string): blog entry that needs to be summarized
	limit (int): number of characters that the summary can include
	"""
	
	import re
	
	regex = re.compile("<[^<>]*?>")
	
	if limit > 0 and text.__len__() >= limit:
		return regex.sub("", text)[:limit] + " [...]"
	
	return regex.sub("", text)