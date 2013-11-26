import web
import program_reader
from whoosh.qparser import QueryParser

urls = (
    '/', 'index', 
    '/indexreal', 'indexreal',
    '/categories', 'categories',
    '/programinfo', 'programinfo',
    '/programinforeal', 'programinforeal',
    '/listview', 'listview',
    '/listviewreal', 'listviewreal',
    '/listviewsearched', 'listviewsearched',
    '/about', 'about',
    '/(js|css|images|fonts)/(.*)', 'static',
)

programs = program_reader.read_programs("programs.json")
search_index = program_reader.whoosh_descriptions(programs)


class index:
    def GET(self):
        render = web.template.render('templates')
        return render.index(render.header(), render.footer())

class indexreal:
    def GET(self):
        render = web.template.render('templates')
        return render.index_real(render.header(), render.footer())
        
class categories:
    def GET(self):
        render = web.template.render('templates')
        return render.categories(render.header(), render.footer())

class programinfo:
    def GET(self):
        render = web.template.render('templates')
        return render.programinfo(render.header(), render.footer())

class programinforeal:
    def GET(self):
        render = web.template.render('templates')
        if web.input()['ind']:
            ind = int(web.input()['ind'])
            return render.programinfo_real(render.header(), render.footer(), programs[ind])

class listview:
    def GET(self):
        render = web.template.render('templates')
        return render.listview(render.header(), render.footer())

class listviewreal:
    def GET(self):
        render = web.template.render('templates')
        return render.listview_real(render.header(), render.footer(), programs)
        
class listviewsearched:
    def GET(self):
        render = web.template.render('templates')
        query = QueryParser("short_desc", search_index.schema).parse(unicode(web.input()['q']))
        results = None
        
        with search_index.searcher() as searcher:
            results = searcher.search(query)
            print results    
            return render.listview_real(render.header(), render.footer(), results)

class about:
    def GET(self):
        render = web.template.render('templates/about')
        return render.about(render.header(), render.footer())

class static:
    def GET(self, media, file):
        try:
            f = open(media+'/'+file, 'r')
            return f.read()
        except:
            return '' # you can send an 404 error here if you want

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
