import web

urls = (
    '/', 'index',
    '/about', 'about',
    '/(js|css|images|fonts)/(.*)', 'static', 
)

class index:
    def GET(self):
        render = web.template.render('templates/')
        return render.index(render.header(), render.footer())

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
