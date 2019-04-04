from rdflib import URIRef, Literal


def to_title(s: str) -> Literal:
	"""
	Turns the argument into a Mediawiki-suitable page title.
	Truncates to first LF/CR or Chinese Character, whichever comes first, then
	Replaces whitespaces by underscores, then prefixes with a column,
	converts to URIRef, and finally removes the < > surrounding it.
	:param s: name of the object
	:return: new name for RDF import into wiki
	"""
	s = s.splitlines()[0]  # keeps first line only
	s = s.strip(" ").strip("(").strip(")")
	# substitutes whitespaces with underscores, and prefixes with local (empty) namespace ":"
	s = URIRef(':' + s.replace(' ', '_'))

	# spot the 1st Chinese (or any other bizarre) character
	for i, char in enumerate(s):
		if ord(char) > 0x7a:
			s = Literal(s[0:i].strip().strip('_'))  # does not work without calling Literal
			break

	return s

def to_name_en(s: str) -> str:
	"""

	:param s:
	:return:
	"""
	return to_title(s)

def to_name_zh(s: str) -> Literal:
	OrdCnStart = 0x4e00
	# start with the 1st Chinese character
	for i, char in enumerate(s):
		if ord(char) >= OrdCnStart:
			s = s[i:]
			return ":" + s
	return ''


# Functions for turning RDF into SMW-import ready RDF

def remove_gt_lt(s: str) -> str:
	"""
	Removes the < and > from URIs in the RDF turtle output.
	First step is to identify first occurrence of a subject in a triple,
	so that @prefix headers remain unaffected.
	:param s: the input text file to be processed
	:return: the RDF-ready file
	"""
	split_string = s.split(sep='<:', maxsplit=1)  # split at first subject; sep will be removed, by the way
	cleaned_string = split_string[0] + ':' + split_string[1].replace('<', '').replace('>', '')
	return cleaned_string


def remove_roo(s: str) -> str:
	"""
	Removes the 'roo' in property designation 'roo:<something>' for import into SMW
	:param s:
	:return:
	"""
	return s.replace('roo:', ':')


def local_Roo(s: str) -> str:
	"""

	:param s:
	:return:
	"""
	return s.replace('<http://webprotege.stanford.edu/project/ErEJMiB9aKwG6oPN4WkYE#>', '<#>')


def prepare_for_SMW_import(s: str) -> str:
	return (local_Roo(remove_roo(remove_gt_lt(s))))

