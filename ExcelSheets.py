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
		# Triples
		self.Graph = RooGraph(identifier='SIG_graph_')
		self.Graph.add((to_title('Signalling Package'), RDF.type, Literal("Domain_Package")))
		self.Graph.add((to_title('Signalling Package'), nsRoo.hasVersion, Literal(version)))


	def get_objects(self):
		pass

	def cast_to_rdf(self, path, fmt='turtle'):
		self.RdfFormat = fmt
		self.Rdf = open(path, 'w+t', newline=None)
		s = str(self.Graph.serialize(format=fmt), 'utf-8')
		s = prepare_for_SMW_import(s)
		print(s)
		outfile = open(path, 'w+t', encoding = 'utf-8', newline=None)
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

	def get_functional_categories(self):
		"""
		In SIG, objects may belong to several functional categories!
		"""
		self.Graph.add((to_title('CBI'), RDF.type, Literal('Functional Category')))
		self.Graph.add((to_title('Block system'), RDF.type, Literal('Functional Category')))
		self.Graph.add((to_title('Train control system'), RDF.type, Literal('Functional Category')))
		self.Graph.add((to_title('Traffic dispatching system'), RDF.type, Literal('Functional Category')))

	def get_objects(self, first_row, last_row, suffix = ''):
		object_count = 0
		for row in self.SheetObj.iter_rows(min_row=first_row, max_row=last_row, min_col=1, max_col=9):
			this_title = URIRef(to_title(row[1].value) + '_--_' + suffix)
			self.Graph.add((this_title, RDF.type, Literal("Object")))
			self.Graph.add((this_title, nsRoo.Has_id, Literal(row[0].value)))
			self.Graph.add((this_title, nsRoo.Has_version, Literal(self.Version)))
			self.Graph.add((this_title, nsRoo.Has_name_en, Literal(to_name_en(row[1].value))))
			self.Graph.add((this_title, nsRoo.Has_name_zh, Literal(to_name_zh(row[1].value))))
			object_count += 1
		print('Total objects added: {}'.format(object_count))



sig = SIG(R'C:\Users\amagn\Desktop\SIG Data\Copy of 20190322-IFC-SD-005-DataRequirement.xlsx',
          '1-Object_Description ', '2.2-Property_Requirements_Spec', '2.1-Property_Requirement_Shared', "0.1")
sig.get_functional_categories()
sig.get_objects(6, 116, suffix = 'sig')
print('\nTotal number of triples in {}: {}\n'.format(sig.Graph.n3(), len(sig.Graph)))
sig.cast_to_rdf(R'C:\Users\amagn\OneDrive\Dev\DataRequirementsToRDF\SIG.ttl')
