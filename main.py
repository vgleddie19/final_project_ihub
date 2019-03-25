import os
import urllib
import jinja2
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras import sessions

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname('templates/')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class Orders():
    details = {
        'customercode':'',
        'smancode':'',
        'address':'',
        'dateorder':''
    }
    products = { }

# Start Model
class User(ndb.Model):
    username = ndb.StringProperty()
    password = ndb.StringProperty()

class Orders(ndb.Model):
    details = ndb.StringProperty()
    items = ndb.StringProperty()
    user  = ndb.StringProperty()
    created_date = ndb.DateTimeProperty(auto_now_add=True)

# End Model

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

    def render(self, template, values={}):
        tpl = JINJA_ENVIRONMENT.get_template(template)
        self.response.write(tpl.render(values))
        return

# Main Handler
class MainPage(BaseHandler):
    def get(self):
        user = self.session.get('user')
        self.render('index.html',{'user':user})
        return
    def post(self):
        get

class Order(BaseHandler):
    def get(self):
        user = self.session.get('user')
        self.render('order.html',{'user':user})
        return
    def post(self):
        username = self.request.get('')
        password = self.request.get('password')
        user = User.query(User.username == username).get()
        if user:
            if user.password == password:
                self.session['user'] = user.username
                self.redirect('/')
                return
            self.redirect('/login?error=1')
            return
        else:
            user = User(
                username=username,
                password=password
            )
            user.put()
            self.redirect('/login?success=1')
        self.redirect('/login')
        return

class Stocks(BaseHandler):
    def get(self):
        user = self.session.get('user')
        self.render('stocks.html',{'user':user})
        return
    def post(self):
        get

class Logout(BaseHandler):
    def get(self):
        del self.session['user']
        self.redirect('/')
        return


class LogIn(BaseHandler):
    def get(self):
        # self.response.write('Hello')
        self.render('login.html')
        return

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        user = User.query(User.username == username).get()
        if user:
            if user.password == password:
                self.session['user'] = user.username
                self.redirect('/')
                return
            self.redirect('/login?error=1')
            return
        else:
            user = User(
                username=username,
                password=password
            )
            user.put()
            self.redirect('/login?success=1')
        self.redirect('/login')
        return
# End Main Handler
# Start app
config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/login', LogIn),    
    ('/logout', Logout),    
    ('/order',Order),
    ('/stocks',Stocks),
], debug=True,
config=config)
# End App
