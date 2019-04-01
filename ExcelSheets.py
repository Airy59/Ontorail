import datetime

import openpyxl
import rdflib
from rdflib import RDF, Literal

from References import nsRoo, RooGraph
from Utils import to_title, remove_gt_lt


class DataReqFile:
	"""
	Ancestor Class for IFC Data Requirements files
	"""

	def __init__(self, path, tab_obj, tab_prop):
		self.Path = path
		self.ImportDateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		self.TabObj = tab_obj
		self.TabProp = tab_prop
		self.Book = openpyxl.load_workbook(self.Path, read_only=True)
		self.SheetObj = self.Book[self.TabObj]
		self.SheetProp = self.Book[self.TabProp]
		self.Rdf = None
		self.RdfFormat = None
		# Triples
		self.Graph = rdflib.Graph(identifier='SIG_graph')

	def get_objects(self):
		pass

	def cast_to_rdf(self, path, fmt='turtle'):
		self.RdfFormat = fmt
		self.Rdf = open(path, 'w+t', newline=None)
		s = str(self.Graph.serialize(format=fmt), 'utf-8')
		s = remove_gt_lt(s)
		print(s)
		outfile = open(path, 'w+t', newline=None)
		outfile.write(s)
		outfile.close()


class SIG(DataReqFile):
	"""
	SIG data requirements
	"""

	def __init__(self, path, tab_obj, tab_prop_spec, tab_prop_shared):
		super().__init__(path, tab_obj, tab_prop_spec)
		self.TabPropShared = tab_prop_shared
		self.SheetPropShared = self.Book[tab_prop_shared]
		self.Graph = RooGraph(identifier='SIG_graph_')

	def get_functional_categories(self):
		"""
		In SIG, objects may belong to several functional categories!
		"""
		self.Graph.add((to_title('CBI'), RDF.type, Literal('Functional Category')))
		self.Graph.add((to_title('Block system'), RDF.type, Literal('Functional Category')))
		self.Graph.add((to_title('Train control system'), RDF.type, Literal('Functional Category')))
		self.Graph.add((to_title('Traffic dispatching system'), RDF.type, Literal('Functional Category')))

	def get_objects(self, first_row, last_row):
		for row in self.SheetObj.iter_rows(min_row=first_row, max_row=last_row, min_col=1, max_col=9):
			self.Graph.add((to_title(row[1].value), nsRoo.hasID, Literal(row[0].value)))


sig = SIG(R'C:\Users\amagn\Desktop\SIG Data\20190322-IFC-SD-005-DataRequirement.xlsx',
          '1-Object_Description ', '2.2-Property_Requirements_Spec', '2.1-Property_Requirement_Shared')
sig.get_functional_categories()
sig.get_objects(6, 116)
print('\nTotal number of triples in {}: {}\n'.format(sig.Graph.n3(), len(sig.Graph)))
sig.cast_to_rdf(R'C:\Users\amagn\OneDrive\Dev\DataRequirementsToRDF\SIG.ttl')
