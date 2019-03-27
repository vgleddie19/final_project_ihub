import os
import urllib
import jinja2
import webapp2
import logging

from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras import sessions

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname('templates/')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

# Start Model
class User(ndb.Model):
    username = ndb.StringProperty()
    password = ndb.StringProperty()

class Products(ndb.Model):
    product = ndb.StringProperty(repeated=True)
    user  = ndb.StringProperty()

    @classmethod
    def create(cls, product, user):
        prod = cls()
        prod.product = product
        prod.user = user
        prod.put()
        return prod
    
    @classmethod
    def update(cls, id, product, user):
        prod = cls.get_by_id(int(str(id)))
        if not prod:
            raise Exception('PRODUCT not found!')
        prod.product = product
        prod.user = user
        prod.put()
        return prod

    @classmethod
    def list_all(cls):
        prod_results = cls.query().fetch()
        results = []
        for prod in prod_results:
            results.append({
                'id': prod.key.id(),
                'product': prod.product
            })

        return results
    
    @classmethod
    def list_product(cls):
        prod_results = cls.query().fetch()
        results = []
        for prod in prod_results:
            results.append({
                'product': prod.product
            })

        return results
    @classmethod
    def remove(cls, id):
        prod = cls.get_by_id(int(str(id)))
        if not prod:
            raise Exception('PRODUCT not found')
        prod.key.delete()
        
    @classmethod
    def remove_all(cls):
        results = cls.query().fetch()
        for idx in results:
            prod = cls.get_by_id(int(str(idx.key.id())))
            if not prod:
                raise Exception('PRODUCT not found')
            prod.key.delete()

class ShippingDetails(ndb.Model):
    details = ndb.StringProperty(repeated=True)
    user  = ndb.StringProperty()

    @classmethod
    def create(cls, details, user):
        sd = cls()
        sd.details = details
        sd.user = user
        sd.put()
        return sd
    
    @classmethod
    def update(cls, id, details, user):
        sd = cls.get_by_id(int(str(id)))
        if not sd:
            raise Exception('Shipping Details not found!')
        sd.details = details
        sd.user = user
        sd.put()
        return sd

    @classmethod
    def list_all(cls):
        sd_results = cls.query().fetch()
        results = []
        for detail in sd_results:
            results.append({
                'id': detail.key.id(),
                'shipping': detail.details
            })

        return results

    @classmethod
    def list_shipping(cls):
        sd_results = cls.query().fetch()
        results = []
        for detail in sd_results:
            results.append({
                'shipping': detail.details
            })

        return results

    @classmethod
    def remove(cls, id):
        detail = cls.get_by_id(int(str(id)))
        if not detail:
            raise Exception('Shipping Details not found')

        detail.key.delete()
        
    @classmethod
    def remove_all(cls):
        results = cls.query().fetch()
        for idx in results:
            detail = cls.get_by_id(int(str(idx.key.id())))
            if not detail:
                raise Exception('Shipping Details not found')
            detail.key.delete()
               
class Orders(ndb.Model):
    details = ndb.StringProperty(repeated=True)
    products = ndb.StringProperty(repeated=True)
    user  = ndb.StringProperty()
    created_date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def create(cls, details, products, user):
        order = cls()
        order.products = products
        order.details = details
        order.user = user
        order.put()
        return order
    
    @classmethod
    def update(cls, id, details, products, user):
        order = cls.get_by_id(int(str(id)))
        if not order:
            raise Exception('ORDER not found!')
        order.details = details
        order.products = products
        order.user = user
        order.put()
        return order

    @classmethod
    def list_all(cls):
        order_results = cls.query().order(
            -cls.created_date).fetch()
        order = []
        for prod in order_results:
            pdetails = list(prod.products)
            for idx, item in enumerate(pdetails):
                r = item.strip('"')
                pdetails[idx] = r

            odetails = list(prod.details)
            for idx, item in enumerate(odetails):
                r = item.strip('"')
                odetails[idx] = r
            
            order.append({
                'details': odetails,
                'products': pdetails,
                'user':prod.user
            })
        return order    

    def remove(cls, id):
        order = cls.get_by_id(int(str(id)))
        if not order:
            raise Exception('ORDER not found')

        order.key.delete()
        return True

    def remove_all(cls):
        for idx in cls().query().fetch():
            order = cls.get_by_id(int(str(idx)))
            if not order:
                raise Exception('ORDER not found')
            order.key.delete()
        return true
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
    def getDashBoardRecord(self):
        results = {
            '1':1,
            '2':2
            }
        return results

    def get(self):
        results = self.getDashBoardRecord()
        template_values = {}
        for item in results:
            template_values.update({'so':item})

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
        return
    def post(self):
        intent = self.request.get('intent')
        if intent == "SAVEORDER":
            prod_results = Products.list_product()
            prodorder = []
            for item in prod_results:
                prodorder.append(str(item))

            ship_results = ShippingDetails.list_shipping()
            shipping = []
            for item in ship_results:
                shipping.append(str(item))

            Orders.create(shipping,prodorder,'Eddie')
            Products.remove_all()
            ShippingDetails.remove_all()

        return self.redirect('/?intent = %s ' % intent)        
        
class OrderProduct(BaseHandler):
    def get(self):
        preorder = Products.list_all()
        template_values = {
            'preorder':preorder
        }
        template = JINJA_ENVIRONMENT.get_template('orderproducts.html')
        self.response.write(template.render(template_values))
    def post(self):
        intent = self.request.get('intent')
        prodid = self.request.get('id')
        sproduct = [
        self.request.get('productcode'),
        self.request.get('description'),
        self.request.get('uom'),
        self.request.get('qty')        
        ]            
        if intent == 'REMOVEPRODUCT':
            Products.remove(prodid)
        else:
            Products.create(sproduct,'Eddie')
        
        return self.redirect('/orderproduct?intent = %s' % intent)               

class Order(BaseHandler):
    def get(self):
        detail = ShippingDetails.list_all()
        template_values = {
            'details':detail
        }
        template = JINJA_ENVIRONMENT.get_template('order.html')
        self.response.write(template.render(template_values))
    def post(self):
        intent = self.request.get('intent')
        detail = ShippingDetails.list_all()
        if not detail:
            details = []
            details.append(self.request.get('shipping[first-name]'))
            details.append(self.request.get('shipping[last-name]'))
            details.append(self.request.get('shipping[address]'))
            details.append(self.request.get('shipping[address-2]'))
            details.append(self.request.get('city'))    
            details.append(self.request.get('country'))
            if details[0]:
                ShippingDetails.create(details,'Eddie')                
        
        return self.redirect('/orderproduct?intent = %s' % intent)        

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
    ('/order',Order),
    ('/orderproduct',OrderProduct),
], debug=True,
config=config)
# End App
