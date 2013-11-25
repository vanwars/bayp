import web
import program_reader

urls = (
    '/', 'index', 
    '/categories', 'categories',
    '/programinfo', 'programinfo',
    '/listview', 'listview',
    '/listviewreal', 'listviewreal',
    '/about', 'about',
    '/(js|css|images|fonts)/(.*)', 'static' 
)

programs = program_reader.read_programs("programs.json")

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
        return render.programinfo(render.header(), render.footer())

class listview:
    def GET(self):
        render = web.template.render('templates')
        return render.listview(render.header(), render.footer())

class listviewreal:
    def GET(self):
        render = web.template.render('templates')
        return render.listview_real(render.header(), render.footer(), programs)

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
