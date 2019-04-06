from rdflib import URIRef, Literal

OrdCnStart = 0x4e00


def to_title(s: str) -> URIRef:
	"""
	Turns the argument into a Mediawiki-suitable page title.
	Truncates to first Chinese Character, then
	Replaces whitespaces by underscores, then prefixes with a column,
	converts to URIRef.
	:param s: name of the object
	:return: new name for RDF import into wiki
	"""

	s = to_name_en(s)

	# substitutes whitespaces with underscores, and prefixes with local (empty) namespace ":"
	s = URIRef(':' + Literal(s.replace(' ', '_')))

	return s


def to_name(s: str) -> Literal:
	"""
	Does some basic transforms in order to make strings found in Excel sheets usable for naming.
	In particular, it replaces brackets: (...) by: --..., as these wreak havoc in RDFIO imports
	:param s:
	:return:
	"""
	s = s.strip(" ").strip("(").strip(")").strip('"').strip("'").replace('\n', ' ').replace('\r', '')
	return Literal(s.replace('(', '--').replace(')', ''))


def to_name_en(s: str) -> Literal:
	"""
	Calls to_name transform, and then gets rid of Chinese characters
	:param s:
	:return:
	"""

	s = to_name(s)

	# spot the 1st Chinese (or any other bizarre) character
	for i, char in enumerate(s):
		if ord(char) > OrdCnStart:
			s = s[0:i].strip().strip('_')
			break

	return Literal(s)


def to_name_zh(s: str) -> Literal:
	"""
	Calls to_name, then retains the substring starting with first encountered Chinese character
	:param s:
	:return:
	"""
	s = to_name(s)
	# start with the 1st Chinese character
	for i, char in enumerate(s):
		if ord(char) >= OrdCnStart:
			s = s[i:].strip()
			return Literal(s)
	# if no Chinese character was found, return an empty string:
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
