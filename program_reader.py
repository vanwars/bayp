import json
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.analysis import *

def read_programs(filename):
    json_data = open(filename)
    data = json.load(json_data)
    json_data.close()    
    return data
    
def whoosh_descriptions(programs):
    schema = Schema(name=TEXT(stored=True), index=ID(stored=True), short_desc=TEXT(stored=True, analyzer=(StandardAnalyzer(minsize=2) | NgramFilter(minsize=3))))
    index = create_in("whooshindex", schema)
    writer = index.writer()
    
    for prog_index in xrange(len(programs)):
        writer.add_document(name=programs[prog_index]["name"], index=unicode(prog_index), short_desc=programs[prog_index]["short_desc"])
    writer.commit()
    
    return index