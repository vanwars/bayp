import web
import program_reader
import tempfile
from whoosh.qparser import QueryParser

urls = (
    '/', 'index', 
    '/categories', 'categories',
    '/programinfo', 'programinfo',
    '/listview', 'listview',
    '/about', 'about',
    '/contact', 'contact',
    '/login', 'login',
    '/logout', 'logout',
    '/register', 'register',
    '/profile', 'profile',
    '/saved', 'saved',
    '/favorite', 'favorite',
    '/(js|css|images|fonts)/(.*)', 'static',
)

programs = program_reader.read_programs("programs.json")
search_index = program_reader.whoosh_descriptions(programs)

app = web.application(urls, globals())

if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'user': 'anonymous'})
    web.config._session = session
else:
    session = web.config._session

class index:
    def GET(self):
        render = web.template.render('templates')
        return render.index(render.header(session.user), render.footer(), session.user)
       
class favorite:
    def GET(self):
        ind = int(web.input()['id'])
        try:
            session['favorites'].append(programs[ind])
        except KeyError:
            session['favorites'] = [programs[ind]]
            
class categories:
    def GET(self):
        render = web.template.render('templates')
        return render.categories(render.header(session.user), render.footer())


class programinfo:
    def GET(self):
        render = web.template.render('templates')
        if web.input()['ind']:
            ind = int(web.input()['ind'])
            return render.programinfo(render.header(session.user), render.footer(), programs[ind])
        
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

            if zipcode == u"":
                zipcode = "*"

            backup_results = searcher.search(backup_query)
            if len(backup_results) == 0:
                backup_query = QueryParser("category", search_index.schema).parse("*")
                backup_results = searcher.search(backup_query)
                
            query = QueryParser("category", search_index.schema).parse("zipcode:"+zipcode+" "+category)
            results = searcher.search(query)
            
            filtered_backups = []
            
            #dedup results
            for i in xrange(10):
                found_match = False
                for j in xrange(10):
                    try:
                        if backup_results[i]['name'] == results[j]['name']:
                            found_match = True
                    except IndexError:
                        continue
                if not found_match:
                    filtered_backups.append(backup_results[i])
                
            return render.listview(render.header(session.user), render.footer(), results, filtered_backups, category, zipcode, session)

class about:
    def GET(self):
        render = web.template.render('templates')
        return render.about(render.header(session.user), render.footer())

class contact:
    def GET(self):
        render = web.template.render('templates')
        return render.contact(render.header(session.user), render.footer())

# User capabilities
users = {'antonio' : 'baseball4ever', 'valerie' : 'password'}

class login:
    def GET(self):
        render = web.template.render('templates')
        error = False
        if session.user == 'anonymous':
            return render.login(render.header(session.user), render.footer(), error, session.user, render.login_form())
        else:
            raise web.seeother('/profile')

    def POST(self):
        render = web.template.render('templates')
        username = web.input().username
        password = web.input().password
        error = False
        if not username in users: 
            error = "This user does not exist. Try again."
            return render.login(render.header(session.user), render.footer(), error, session.user, render.login_form())
        elif not username or not password: 
            error = "You must enter a username and a password"
            return render.login(render.header(session.user), render.footer(), error, session.user, render.login_form())
        elif username in users and users[username] == password:
            session.user = username
            raise web.seeother('/profile')

class logout:
    def GET(self):
        session.kill()
        raise web.seeother('/')

class profile:
    def GET(self):
        render = web.template.render('templates')
        if session.user == 'anonymous':
            raise web.seeother('/login')
        else:
            return render.profile(render.header(session.user), render.footer(), session.user)

class saved:
    def GET(self):
        render = web.template.render('templates')
        if session.user == 'anonymous':
            raise web.seeother('/login')
        else:
            saved = programs[0:3]
            i = 1
            for key in saved:
                key['index'] = i
                i += 1
            
            try:
                favorites = session['favorites']
                for i in xrange(len(favorites)):
                    favorites[i]['index'] = i
            except KeyError:
                favorites = []
                
            return render.saved(render.header(session.user), render.footer(), favorites)    

class static:
    def GET(self, media, file):
        try:
            f = open(media+'/'+file, 'r')
            val = f.read()
            f.close()
            return val

        except:
            return '' # you can send a 404 error here if you want

if __name__ == "__main__":
    app.run()
