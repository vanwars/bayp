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
                    address=TEXT(stored=True), \
                    category=TEXT(stored=True), \
                    zipcode=TEXT(stored=True), \
                    school=TEXT(stored=True, analyzer=(StandardAnalyzer(minsize=2) | NgramFilter(minsize=3))))
    index = create_in("whooshindex", schema)
    writer = index.writer()
    
    for prog_index in xrange(len(programs)):
        program = programs[prog_index]
        
        if "address" not in program:
            program["address"] = u"No address provided."
        
        writer.add_document(name=program["name"], \
                            index=unicode(prog_index), \
                            address=program["address"], \
                            category=program["categories"], \
                            zipcode=unicode(program["zipcode"]), \
                            school=program["school"])
    writer.commit()
    
    return index