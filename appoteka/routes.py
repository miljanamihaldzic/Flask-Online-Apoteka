import secrets
import os
from PIL import Image
from flask import render_template,redirect,flash,url_for,session,logging, request,jsonify
from appoteka import app,db, bcrypt
from appoteka.forms.register import RegisterForm
from appoteka.forms.login import LoginForm
from appoteka.forms.account import AccountForm
from appoteka.forms.category import CategoryForm
from appoteka.forms.product import ProductForm
from appoteka.forms.order import OrderForm
from appoteka.models.role import Role
from appoteka.models.user import User
from appoteka.models.category import Category
from appoteka.models.product import Product
from appoteka.models.cart_item import Cart_Item
from appoteka.models.order import Order
from flask_login import login_user, current_user,logout_user,login_required


@app.route('/')
def index():
    my_user = current_user
    categories = Category.query.all()
    return render_template('home.html',my_user = my_user, categories = categories)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register',methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(email = form.email.data, username = form.username.data, role_id = 2,
         password = bcrypt.generate_password_hash(form.password.data).decode('utf-8'))
        db.session.add(user)
        db.session.commit()
        flash('You are now register and can log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html',form = form)


@app.route('/login', methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm(request.form)
    if form.validate():
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user, remember = form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('index'))
            else:
                flash('Login Unsuccessful. Wrong password.', 'danger')
        else:
            flash('Login Unsuccessful. No user with that username', 'danger')
    return render_template('login.html', form = form)

@app.route('/categories')
def categories():
    categories =Category.query.all()
    return render_template('categories.html',categories = categories)

@app.route('/buy', methods=['POST'])
def buy():
    cart_item = Cart_Item.query.filter_by(user_id = current_user.id, product_id = request.form['product']).first()
    if cart_item:
        cart_item.quantity = cart_item.quantity +1
        db.session.commit()
    else:
        cart_item = Cart_Item(product_id = request.form['product'], user_id = current_user.id)
        db.session.add(cart_item)
        db.session.commit()
    product = Product.query.get(request.form['product'])
    return jsonify({'result':'success', 'product':product.name})
    
#@app.route('/is_empty', methods=['POST'])
#def is_empty():
#    cart_item = Cart_Item(is_active == True, user_id = current_user.id).count()
#    if cart_item==0:
#        return jsonify('is_Empty':'true')
#    else
#        return jsonify('is_Empty':'false')
        


@app.route('/products/<string:id>')
def products(id):
    cat= Category.query.get(id)
    products = Product.query.filter_by(category_id = id)
    return render_template('products.html', products = products, c = cat)

def create_cart_item(product_id):
    cart_item = Cart_Item(product_id = product_id, user_id = current_user.id)
    db.session.add(cart_item)
    db.session.commit()

@app.route('/product/<string:id>', methods=['GET','POST'])
def product(id):
    product = Product.query.get(id)
    return render_template('product.html',product = product)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/cart', methods=['GET','POST'])
@login_required
def cart():
    prod = db.session.query(Cart_Item,Product).outerjoin(Product).filter(Cart_Item.user_id == current_user.id, Cart_Item.is_active == True).all()
    total = 0
    for p in prod:
        total = total +  p[0].quantity * p[1].price
    return render_template('cart.html',prod = prod,total = total)

@app.route('/orders', methods=['GET','POST'])
@login_required
def orders():
    orders = Order.query.distinct()
    return render_template('orders.html',orders = orders)

@app.route('/checkout', methods=['GET','POST'])
@login_required
def checkout():
    form = OrderForm(request.form)
    form.username.data = current_user.username
    form.email.data = current_user.email
    if request.method == "POST":
        prod = db.session.query(Cart_Item,Product).outerjoin(Product).filter(Cart_Item.user_id == current_user.id, Cart_Item.is_active == True).all()
        for p in prod:
            ci = Cart_Item.query.get(p[0].id)
            ci.is_active = False
            o = Order(cart_item_id = ci.id,
                    name = form.first_name.data,
                    last_name = form.last_name.data,
                    username = form.username.data,
                    email = form.email.data,
                    address = form.address.data,
                    country = form.country.data,
                    zip_code = form.zip_code.data,
                    payment_method = form.payment_method.data,
                    name_on_card = form.name_on_card.data,
                    credit_card_number = form.credit_card_number.data,
                    expiration = form.expiration.data,
                    cvv = form.cvv.data)
            db.session.add(o)
            db.session.commit()    
        flash( 'Successful order', 'success')
        return redirect(url_for('index')) 
    prod = db.session.query(Cart_Item,Product).outerjoin(Product).filter(Cart_Item.user_id == current_user.id, Cart_Item.is_active == True).all()
    total = 0
    for p in prod:
        total = total +  p[0].quantity * p[1].price
    return render_template('checkout.html',prod = prod,total = total,form = form)

@app.route('/cart/<string:iddd>/<string:action>', methods=['GET','POST'])
@login_required
def cart1(iddd,action):
    if action == '+':
        ci = Cart_Item.query.get(iddd)
        ci.quantity = ci.quantity +1
        db.session.commit()
    if action == '-':
        ci = Cart_Item.query.get(iddd)
        ci.quantity = ci.quantity -1
        if ci.quantity == 0:
            db.session.delete(ci)
        db.session.commit()
    if action == 'delete':
        ci = Cart_Item.query.get(iddd)
        db.session.delete(ci)
        db.session.commit()
    prod = db.session.query(Cart_Item,Product).outerjoin(Product).filter(Cart_Item.user_id == current_user.id).all()
    total = 0
    for p in prod:
        total = total + p[0].quantity * p[1].price
    return render_template('cart.html',prod = prod, total = total)



def save_picture_resize(form_picture):
    randon_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = randon_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn)

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    return picture_fn


def save_picture(form_picture,folder):
    randon_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = randon_hex + f_ext
    picture_path = os.path.join(app.root_path,'static', folder ,picture_fn)
    print(picture_path)
    form_picture.save(picture_path)
    return picture_fn
    
    
@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = AccountForm(request.form)
    if request.method == 'POST':
        if form.picture.data:
            picture_file = save_picture_resize(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method== 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename = 'profile_pics/' + current_user.image_file)
    return render_template('account.html', image_file= image_file, form = form)

@app.route('/category/new', methods=['GET','POST'])
@login_required
def new_category(): 
    form = CategoryForm(request.form)
    if request.method == 'POST':
        print(form.picture.data)
        if form.picture.data:
            picture_file = save_picture(form.picture.data,'category_pics')
            category = Category(name = form.name.data, description = form.description.data, image_file = picture_file)
        else:
            category = Category(name = form.name.data, description = form.description.data)
        #category = Category(name = form.name.data, description = form.description.data, image_file = 'equipment.jpg')
        db.session.add(category)
        db.session.commit()
        flash('You added new category', 'success')
        return redirect(url_for('categories'))
    else:
        return render_template('category_new.html', form = form)


@app.route('/product/new', methods=['GET','POST'])
@login_required
def new_product():
    form = ProductForm(request.form)
    form.category.choices=[(c.category_id,c.name) for c in Category.query.all()]
    if request.method == 'POST':
        category = Category.query.filter_by(category_id = form.category.data).first()
        if form.picture.data:
            picture_file = save_picture(form.picture.data,'product_pics')
            product = Product(name = form.name.data, description = form.description.data,price = form.price.data, image_file = picture_file,category_id = category.category_id)
        else:
            product = Product(name = form.name.data, description = form.description.data,price = form.price.data,category_id = category.category_id)
        #product = Product(name = form.name.data, description = form.description.data,price = form.price.data, image_file = 'stetoskop.jpg',category_id = category.category_id)
        db.session.add(product)
        db.session.commit()
        flash('You added new Product', 'success')
        return redirect(url_for('products',id = 0))
    else:
        return render_template('product_new.html', form = form)


