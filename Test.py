import rdflib
from rdflib import RDF, RDFS, XSD, BNode, Literal
from rdflib.namespace import Namespace, NamespaceManager

# Binding with Railway Objects Semantic Dictionary ontology
MyProtegeRoot = 'http://webprotege.stanford.edu/project/ErEJMiB9aKwG6oPN4WkYE#'
nsRoo = Namespace(MyProtegeRoot)


class RooGraph(rdflib.Graph):
	def __init__(self, identifier=None):
		super().__init__(store='default', identifier=identifier)
		self.bind("roo", nsRoo)
		self.bind("rdf", RDF)
		self.bind("rdfs", RDFS)
		self.bind("xsd", XSD)


# Create graph (triple store)
MyGraph = RooGraph()

# Local stuff

namespace_manager = NamespaceManager(MyGraph)

# TODO: Load graph from Excel
# ...

# Add some triples manually
# balise = BNode('balise')
balise = Literal(':TestBalise9')
pole = BNode('pole')
ElementType = BNode('ElementType')
Antenna = BNode('antenna')
polarization = BNode('polarization')
print('polarization blank node : ', polarization.n3(namespace_manager), '\n')

MyGraph.add((balise, RDF.type, Literal("Object")))
MyGraph.add((balise, RDFS.label, Literal("Balise (signalling)", lang='en')))
MyGraph.add((balise, RDFS.label, Literal("Balise (signalisation)", lang='fr')))
MyGraph.add((balise, nsRoo.ElementType, Literal("O")))

# MyGraph.add((Antenna, nsRoo.hasProperty, polarization))
#
# MyGraph.add((pole, RDFS.label, Literal("Pole", lang='en')))
# MyGraph.add((pole, RDFS.comment, Literal("some pole or mast")))

# Save (serialize) graph
s = str(MyGraph.serialize(format='turtle'), 'utf-8')
print(s)
outfile = open("testTurtle.ttl", 'w+t', newline=None)
outfile.write(s)
outfile.close()
