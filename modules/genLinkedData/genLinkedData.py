#!/usr/bin/env python3
# coding=utf-8

from .ImportToOnto import *

import time

config = {
    'wantdiff': False,
    'wantsfiles': False,
    'threadsafe': False
}

def createRDFGraph(context):
    graphfilepath = get_output(context)

    # load graph
    graph = Graph()
    graph.open(graphfilepath, create=False)

    # import 101companies and create 101ontology
    ito = ImportToOnto(context, graph)
    ito.do_import()

    # check integrity and display warnings
    ito.check_integrity()

    # print count
    print ('graph has ' + str(len(ito.graph)) + ' entities.')

    # export graph
    ito.save(graphfilepath, "turtle")
    #ito.save(graphfilepath, "xml")
    #ito.save(graphfilepath, "n3")
    #ito.save(graphfilepath, "foo")

def get_output(context):
    return os.path.join(context.get_env('dumps101dir'), 'ontology')

def run(context):
    start_time = time.time()

    createRDFGraph(context)

    print("--- %s ms ---" % ((time.time() - start_time)*1000))
