"""
Excel-to-RDF transformation classes.
"""

import datetime

import openpyxl
from rdflib import RDF, Literal, URIRef

from References import nsRoo, RooGraph
from Utils import to_title, to_name_en, to_name_zh, prepare_for_SMW_import


class DataReqFile:
	"""
	Ancestor Class for IFC Data Requirements files
	"""

	def __init__(self, path, tab_obj, tab_prop, version):
		self.Path = path
		self.ImportDateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		self.TabObj = tab_obj
		self.TabProp = tab_prop
		self.Book = openpyxl.load_workbook(self.Path, read_only=True)
		self.SheetObj = self.Book[self.TabObj]
		self.SheetProp = self.Book[self.TabProp]
		self.Version = version
		self.Rdf = None
		self.RdfFormat = None
		self.DomainPackages = {'Sig': 'Signalling Package', 'Tra': 'Track Package', 'Tel': 'Telecom Package', 'Ene': 'Energy Package'}
		# Triples
		self.Graph = RooGraph(identifier='IFC_Data_Req_')
		for dp in self.DomainPackages.values():
			self.Graph.add((to_title(dp), RDF.type, Literal("Domain_Package")))
			self.Graph.add((to_title(dp), nsRoo.HasVersion, Literal(version)))
			self.Graph.add((to_title(dp), nsRoo.HasNameEn, Literal(dp)))
			self.Graph.add((to_title(dp), nsRoo.HasWikitext, Literal(R"Functional categories in this Domain Package: {{{{#ask: [[Category:Functional Category]] [[InDomainPackage::{}]] }}}}".format(dp)) ))

	def get_objects(self):
		pass

	def cast_to_rdf(self, path, fmt='turtle'):
		self.RdfFormat = fmt
		self.Rdf = open(path, 'w+t', newline=None)
		s = str(self.Graph.serialize(format=fmt), 'utf-8')
		s = prepare_for_SMW_import(s)
		outfile = open(path, 'w+t', encoding='utf-8', newline=None)
		outfile.write(s)
		outfile.close()


class SIG(DataReqFile):
	"""
	SIG data requirements
	"""

	def __init__(self, path, tab_obj, tab_prop_spec, tab_prop_shared, version):
		super().__init__(path, tab_obj, tab_prop_spec, version)
		self.TabPropShared = tab_prop_shared
		self.SheetPropShared = self.Book[tab_prop_shared]
		self.Functional_Categories_Columns = {6: 'CBI', 7: 'Block system', 8: 'Train control system',
		                                      9: 'Traffic dispatching system'}
		# note that curly braces must be doubled to be escaped, herebelow:
		self.Functional_Categories_FreeText = R"Objects belonging to this category: {{{{#ask: [[Category:Object]] [[InFunctionalCategory::{}]] | ?HasNameZh }}}}"


	def set_functional_categories(self):
		"""
		In SIG, objects may belong to several functional categories!
		The categories themselves are not read from the sheets;
		however, the assignment of objects to categories is documented in the sheets and imported here
		"""
		for v in self.Functional_Categories_Columns.values():
			this_title = to_title(v)
			self.Graph.add((this_title, RDF.type, Literal('Functional Category')))
			self.Graph.add((this_title, nsRoo.HasNameEn, Literal(to_name_en(v))))
			self.Graph.add((this_title, nsRoo.InDomainPackage, Literal('Signalling Package')))
			self.Graph.add((this_title, nsRoo.HasWikitext, Literal(self.Functional_Categories_FreeText.format(v))))

	def get_objects(self, first_row, last_row, suffix=''):
		"""
		Scrutinize row after row in selected range.
		:param first_row: first object row
		:param last_row: last object row
		:param suffix: allows to ad suffix to object names, for collision avoidance
		:return:
		"""

		object_count = 0
		# One object at a time...
		for row in self.SheetObj.iter_rows(min_row=first_row, max_row=last_row, min_col=1, max_col=9):
			this_title = URIRef(to_title(row[1].value) + '_--_' + suffix)
			self.Graph.add((this_title, RDF.type, Literal("Object")))
			self.Graph.add((this_title, nsRoo.HasId, Literal(row[0].value)))
			self.Graph.add((this_title, nsRoo.HasVersion, Literal(self.Version)))
			self.Graph.add((this_title, nsRoo.HasNameEn, Literal(to_name_en(row[1].value))))
			self.Graph.add((this_title, nsRoo.HasNameZh, Literal(to_name_zh(row[1].value))))
			for col, fc in self.Functional_Categories_Columns.items():
				# caution: tuple is 0-based, while columns are 1-based...
				if 'x' in str(row[col - 1].value).lower():
					self.Graph.add((this_title, nsRoo.InFunctionalCategory, Literal(fc)))

			object_count += 1

		return (object_count, len(self.Graph))


sig = SIG(R'C:\Users\amagn\Desktop\SIG Data\Copy of 20190322-IFC-SD-005-DataRequirement.xlsx',
          '1-Object_Description ', '2.2-Property_Requirements_Spec', '2.1-Property_Requirement_Shared', "0.1")
result = sig.set_functional_categories()
#result = sig.get_objects(6, 116, suffix='sig')
#print('\nTotal number of objects in {}: {}'.format(sig.Graph.n3(), result[0]))
#print('Total number of triples: {}\n'.format(result[1]))
sig.cast_to_rdf(R'C:\Users\amagn\OneDrive\Dev\DataRequirementsToRDF\SIG.ttl')
