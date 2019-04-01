from rdflib import URIRef

def to_title(s:str) -> str:
	"""
	Replaces whitespaces by underscores, then prefixes with a column,
	converts to URIRef, and finally removes the < >
	:param s: name of the object
	:return: new name for RDF import into wiki
	"""
	s = URIRef(':' + s.replace(' ', '_'))
	#s = s[1:-1]

	return s

def remove_gt_lt(s: str) -> str:
	"""
	Removes the < and > from the RDF turtle output.
	First step is to identify first occurrence of a subject
	:param s: the input text file to be processed
	:return: the RDF-ready file
	"""
	split_string = s.split(sep='<:', maxsplit= 1)
	cleaned_string = split_string[0] + ':' + split_string[1].replace('<', '').replace('>', '')
	return cleaned_string