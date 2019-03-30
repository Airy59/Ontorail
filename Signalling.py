import rdflib
from rdflib import RDF, RDFS, XSD, BNode, Literal
from rdflib.namespace import Namespace, NamespaceManager

# Create graph (triple store)
MyGraph = rdflib.Graph()

# Binding with Railway Objects Semantic Dictionary ontology
rooNs = Namespace('http://webprotege.stanford.edu/project/ErEJMiB9aKwG6oPN4WkYE')
MyGraph.bind("roo", rooNs)

# shorthands for upper ontologies
MyGraph.bind("rdf", RDF)
MyGraph.bind("rdfs", RDFS)
MyGraph.bind("xsd", XSD)

# Local stuff
MyGraph.bind("", "http://mybase")

namespace_manager = NamespaceManager(MyGraph)

# TODO: Load graph from Excel

# Add some triples manually
balise = BNode('balise')
pole = BNode('pole')
ElementType = BNode('ElementType')
Antenna = BNode('antenna')
polarization = BNode('polarization')

MyGraph.add((balise, RDFS.label, Literal("Balise (signalling)", lang='en')))
MyGraph.add((balise, ElementType, Literal("O")))

MyGraph.add((Antenna, rooNs.hasProperty, polarization))

MyGraph.add((pole, RDFS.label, Literal("Pole", lang='en')))
MyGraph.add((pole, RDFS.comment, Literal("some pole or mast")))

# Save (serialize) graph
s = MyGraph.serialize(format='turtle', n)
print(s)
outfile = open("testTurtle.ttl", 'w+t', newline=None)
outfile.write(str(s))
outfile.close()
