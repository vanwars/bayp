import web
import program_reader
from whoosh.qparser import QueryParser

urls = (
    '/', 'index', 
    '/categories', 'categories',
    '/programinfo', 'programinfo',
    '/listview', 'listview',
    '/about', 'about',
    '/contact', 'contact',
    '/login', 'login',
    '/profile', 'profile',
    '/(js|css|images|fonts)/(.*)', 'static',
)

programs = program_reader.read_programs("programs.json")
search_index = program_reader.whoosh_descriptions(programs)


class index:
    def GET(self):
        render = web.template.render('templates')
        return render.index(render.header(), render.footer())
        
class categories:
    def GET(self):
        render = web.template.render('templates')
        return render.categories(render.header(), render.footer())


class programinfo:
    def GET(self):
        render = web.template.render('templates')
        if web.input()['ind']:
            ind = int(web.input()['ind'])
            return render.programinfo(render.header(), render.footer(), programs[ind])
        
class listview:
    def GET(self):
        render = web.template.render('templates')
        zipcode = unicode(web.input()['zip'])
        category = unicode(web.input()['cat'])
        results = None
        backup_results = None
        with search_index.searcher() as searcher:
            backup_query = QueryParser("category", search_index.schema).parse(category)
        
            if category == u"all":
                category=""
                backup_query = QueryParser("category", search_index.schema).parse("*")

            backup_results = searcher.search(backup_query)
                
            query = QueryParser("category", search_index.schema).parse("zipcode:"+zipcode+" "+category)
            results = searcher.search(query)
            results.filter(backup_results)
            return render.listview(render.header(), render.footer(), results, category, zipcode)

class about:
    def GET(self):
        render = web.template.render('templates')
        return render.about(render.header(), render.footer())

class contact:
    def GET(self):
        render = web.template.render('templates')
        return render.contact(render.header(), render.footer())

class login:
    def GET(self):
        render = web.template.render('templates')
        return render.login(render.header(), render.footer())

class profile:
    def GET(self):
        render = web.template.render('templates')
        return render.profile(render.header(), render.footer())     

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
