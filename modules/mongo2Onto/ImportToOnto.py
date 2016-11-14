#!/usr/bin/env python3
# coding=utf-8

import os

try:
    from pymongo import MongoClient
    from bson.json_util import dumps
    from bson.son import SON
except ImportError:
    print('Error: pymongo is missing: "pip3 install pymongo"')

try:
    from rdflib import ConjunctiveGraph, Graph, URIRef, BNode, Literal, RDF, Namespace
    from rdflib.plugins.serializers import turtle, n3, rdfxml
    from rdflib.store import NO_STORE, VALID_STORE
    from rdflib.namespace import FOAF, DC, RDFS
    from urllib import parse as urlparse
except ImportError:
    print('Error: rdflib is missing: "pip3 install rdflib"')

try:
    from graphviz import Digraph
except ImportError:
    print('Error: graphviz is missing: "pip3 install graphviz"')

class printcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ImportToOnto(object):

    def __init__(self, _worker_context, _graph, debug=None):

        self.cur_id = 0

        if(debug is None):
            debug = False
        self.debugmode = debug
        self.context = _worker_context
        self.graph = _graph
        self.labeled_entities = []
        self.pageurl = "http://101companies.org/"
        if self.debugmode:
            self.pageurl = "http://localhost:3000/"

        self.prepare_graph()

    def prepare_graph(self):
        # bind 101 vocabulary
        ns101 = Namespace(self.pageurl + "resource/")
        self.graph.bind("ns101", ns101) # Namespace 101

        # bind externes vocabulary
        self.graph.bind("dc", DC)
        self.graph.bind("foaf", FOAF)

    def get_onto_uriref(self, name):
        #name = name.replace(".", "_")
        name = name.strip().replace(" ", "_")
        #name = name.replace("101", "the101")
        #name = name.lower()
        return URIRef(self.pageurl + "resource/" + urlparse.quote(name))

    def do_import(self):
        # do collection of manuelly imports e.g. static objects
        self.do_manually_import()

        # do imports e.g. reading dumps or filestructures
        self.do_automatic_import()

    def do_manually_import(self):
        # 101 vocabulary entities
        self.addLabel("101worker")
        self.addToGraph("101worker", FOAF.isPrimaryTopicOf, Literal("http://101companies.org/wiki/101worker"), 'import_workermodules_init')
        self.addToGraph("101worker", URIRef('http://purl.org/dc/terms/abstract'), Literal("Computational component of the infrastructure of the 101project"), 'import_workermodules_init')

        self.addToGraph("uses", RDFS.comment, Literal("The subject uses the object."), 'prepare_graph')
        self.addToGraph("instanceof", RDFS.comment, Literal("The subject is an instance of the object."), 'prepare_graph')
        self.addToGraph("memberof", RDFS.comment, Literal("The subject member the object."), 'prepare_graph')

    def do_automatic_import(self):
        self.import_wikipages()
        self.import_workermodules()
        self.import_repo()
        self.import_resources_and_dumps()
        self.import_conceptual_data()

    def import_repo(self):
        self.msg ("import repo into graph", printcolors.OKBLUE)

        self.msg ("done", printcolors.OKBLUE)

    def import_workermodules(self):
        self.msg ("import worker and modules into graph", printcolors.OKBLUE)

        module_counter = 0
        for root, dirs, files in os.walk(self.context.get_env("modules101dir")):
            for file in files:
                if file.endswith("__init__.py"):
                    txt = open(os.path.join(root, file))

                    module_counter = module_counter + 1
                    module_name = root.split('/')[-1]
                    self.msg("import module: " + module_name, printcolors.ENDC, 1)
                    self.addLabel(module_name)
                    self.addToGraph(module_name, RDF.type, "101worker module", 'import_workermodules')
                    self.addToGraph(module_name, DC.isPartOf, "101worker", 'import_workermodules')
                    self.addToGraph(module_name, DC.requires, "101worker", 'import_workermodules')
        self.msg (str(module_counter) + " modules imported", printcolors.ENDC, 1)

        self.msg ("done", printcolors.OKBLUE)

    def import_resources_and_dumps(self):
        self.msg ("import resources and dumps into graph", printcolors.OKBLUE)

        self.msg ("done", printcolors.OKBLUE)

    def import_wikipages(self):
        self.msg ("import wikipages into graph", printcolors.OKBLUE)
        wiki_links_json = self.context.read_dump('wiki-links')

        pages = wiki_links_json['wiki']['pages']
        types = ['Contribution',
                 'Contributor',
                 'Technology',
                 'Language',
                 'Features']

        for t in types:
            filtered  = filter(lambda p: t == p.get('p', ''), pages)
            for f in filtered:
                subj = self.getentityname(self.getentityname(f['n'], f['p']), 'wikipage')

                self.addToGraph(subj, FOAF.isPrimaryTopicOf, Literal("http://101companies.org/wiki/" + f['p'] + ":" + f['n'].strip().replace(' ','_')), 'import_wikipages')
                self.addToGraph(subj, FOAF.isPrimaryTopicOf, self.getentityname(f['n'], f['p']), 'import_wikipages')

                self.scan('Uses', f)
                #self.scan('mentions', f)
                #self.scan('LinksTo', f) # LinksTo is a wikipedia-link or mabye a github 101repo link
                self.scan('InstanceOf', f)
                self.scan('MemberOf', f)

        self.msg ("done", printcolors.OKBLUE)

    def import_conceptual_data(self):
        self.msg ("import conceptual data into graph", printcolors.OKBLUE)

        self.msg ("done", printcolors.OKBLUE)

    def scan(self, t, item):
        if (t in item):
            for u in item[t]:
                #self.msg("  " + t + " " + u['n'])
                if ('p' in u and str(u['p']) != 'None'):
                    subj = self.getentityname(u['n'], u['p'])
                    self.addLabel(subj, u['n'])

                    subj_type = self.getentityname(u['p'])

                    item_name = self.getentityname(item['n'], item['p'])
                    item_type = self.getentityname(item['p'])

                    self.addToGraph(subj, RDF.type, subj_type, 'scan_' + t + '1')

                    self.addToGraph(item_name, RDF.type, item_type, 'scan_' + t + '2')
                    self.addToGraph(item_name, t.lower(), subj, 'scan_' + t + '3')

    def getentityname(self, subjname, typename = None):
        if(typename):
            return typename.lower() + "-" + subjname.lower()
        else:
            return subjname.lower()

    def addToGraph(self, s, p, o, debuginfo, create_label = True):

        if (self.debugmode):
            self.graph.add(
                (self.get_onto_uriref(s),
                 self.get_onto_uriref('importedBy'),
                 self.get_onto_uriref(debuginfo))
            )
            self.graph.add(
                (self.get_onto_uriref(debuginfo),
                 RDF.type,
                 self.get_onto_uriref('import_method'))
            )
            self.graph.add(
                (self.get_onto_uriref(debuginfo),
                 DC.isPartOf,
                 self.get_onto_uriref('mongo2onto'))
            )

        if(not isinstance(o, Literal) and isinstance(o, str)):
            o = self.get_onto_uriref(o)
        if not isinstance(p, URIRef):
            p = self.get_onto_uriref(p)

        self.graph.add((self.get_onto_uriref(s), p, o))

        if self.debugmode:
            need_id = True
            for id in self.graph.objects(self.get_onto_uriref(s), self.get_onto_uriref('ontoid')):
                need_id = False

            if need_id:
                self.cur_id = self.cur_id + 1
                self.graph.add((self.get_onto_uriref(s), self.get_onto_uriref('ontoid'), Literal(self.cur_id)))

    def addLabel(self, entity, label = None):

        if label == None:
            label = entity

        if(entity not in self.labeled_entities):
            self.labeled_entities.append(entity)
            self.graph.add((self.get_onto_uriref(entity), DC.label, Literal(label)))

    def msg(self, txt, txtcolor = printcolors.ENDC, level = 0):
        if(self.debugmode):
            print (txtcolor + ('  ' * (level + 1)) + txt + printcolors.ENDC)

    def check_integrity(self):
        self.msg("checking integrity now", printcolors.OKBLUE)

        # Recognize similar objects

        # check predicates, which are to be used once
        single_use_predicats = [
            DC.label,
            URIRef('http://purl.org/dc/terms/abstract'),
            self.get_onto_uriref('instanceof'),
            RDF.type
        ]

        checked_subjects = []
        for s in self.graph.subjects():
            if s not in checked_subjects:
                checked_subjects.append(s)
                for pred in single_use_predicats:
                    tmp = []
                    for o in self.graph.objects(s, pred):
                        if(o not in tmp):
                            tmp.append(o)
                            if (len(tmp) == 2):
                                self.msg(str(s) + ' has multiple ' + str(pred) + "(" + str(o), printcolors.WARNING, 1)

        self.msg("done", printcolors.OKBLUE)

    def save(self, output_path, export_format):
        if (export_format == "turtle"):
            s = turtle.TurtleSerializer(self.graph)
            out = open(output_path + '.ttl', 'wb')
        elif (export_format == "xml"):
            s = rdfxml.XMLSerializer(self.graph)
            out = open(output_path + '.xml', 'wb')
        elif (export_format == "n3"):
            s = n3.N3Serializer(self.graph)
            out = open(output_path + '.n3', 'wb')
        else:
            raise Exception('unknown export format "' + export_format + '"!')
        s.serialize(out)

        self.msg('export done with format "' + export_format + '"', printcolors.OKGREEN)
