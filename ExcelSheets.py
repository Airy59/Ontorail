import datetime

import openpyxl

import rdflib
from rdflib import RDF, RDFS, XSD, BNode, Literal

from Test import MyProtegeRoot, nsRoo, RooGraph


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


class SIG(DataReqFile):
	"""
	SIG data requirements
	"""

	def __init__(self, path, tab_obj, tab_prop_spec, tab_prop_shared):
		super().__init__(path, tab_obj, tab_prop_spec)
		self.TabPropShared = tab_prop_shared
		self.SheetPropShared = self.Book[tab_prop_shared]

	def get_functional_categories(self):
		"""
		In SIG, objects may belong to several functional categories!
		"""


	def get_objects(self, first_row, last_row):
		for row in self.SheetObj.iter_rows(min_row=first_row, max_row=last_row,min_col=1, max_col=)





sig = SIG(R'C:\Users\amagn\Desktop\SIG Data\20190322-IFC-SD-005-DataRequirement.xlsx',
          '1-Object_Description ', '2.2-Property_Requirements_Spec', '2.1-Property_Requirement_Shared')








