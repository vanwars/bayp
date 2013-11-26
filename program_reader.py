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
    schema = Schema(name=TEXT(stored=True), \
                    index=ID(stored=True), \
                    address=TEXT, \
                    zipcode=TEXT(stored=True), \
                    short_desc=TEXT(stored=True, analyzer=(StandardAnalyzer(minsize=2) | NgramFilter(minsize=3))))
    index = create_in("whooshindex", schema)
    writer = index.writer()
    
    for prog_index in xrange(len(programs)):
        program = programs[prog_index]
        writer.add_document(name=program["name"], \
                            index=unicode(prog_index), \
                            address=program["address"], \
                            zipcode=unicode(program["zipcode"]), \
                            short_desc=program["short_desc"])
    writer.commit()
    
    return index