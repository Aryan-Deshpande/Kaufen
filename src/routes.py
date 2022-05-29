from crypt import methods
from curses import meta
from src import app,loginmanager
from flask import redirect, render_template, request, url_for
from src import Item,User
from src.forms import RegisterForm
from src import db
from src.forms import LoginForm,Purch,Sell
from flask_login import login_required, login_user, current_user,logout_user

@loginmanager.user_loader # this here is a callback
def load_user(user_id):                                 # FUNCTION THAT TAKES A USER ID, TO ASSOCIATE WITH SESSION ID
    return User.query.get(int(user_id))                 # RETURNS CORRESPONDING USER OBJECT FROM USER ID STORED IN THE SESSION

@app.route('/')
def home_page():
    return render_template('home.html')

@login_required
@app.route('/market/')
def market_page():                                              # API TO RENDER DETIALS FOR ITEMS OWNED && NOT OWNED
    items = Item.query.filter_by(owner=None)                    # FILTERED ITEMS NOT OWNED BY USER
    owned = Item.query.filter_by(owner=current_user.id)         # FILTERED ITEMS OWNED BY USER
    #items = [{"name":"Watch","price":2000,"category":"Accessories"},{"name":"Football","price":344,"category":"Sports"},{"name":"GODOFWAR","price":12,"category":"VideoGame"}]
    return render_template('market.html',items=items,owned=owned)

@app.route('/register/', methods=['GET', 'POST'])
def register_page():                                                # REGISTRATION FORM #
    form = RegisterForm()                                           # CREATING FORM FOR REGISTRATION
    if request.method =="POST":
        if form.validate_on_submit():                               # WHEN FORM IS SUBMITTED IF CONDITION RUNS
            user_to_create = User(name=form.username.data,          # QUERY TO CREATE A NEW USER
                                email=form.email.data,
                                passh=form.password1.data)
            db.session.add(user_to_create)                          # ADDING TO DB  
            db.session.commit()                                     # COMMITING TO DB
            login_user(user_to_create)                              # LOGGING IN USER DIRECTLY,  WITH THE USER OBJECT
            return redirect(url_for('market_page'))
            
        if form.errors != {}: #If there are not errors from the validations
            for err_msg in form.errors.values():
                print(f'There was an error with creating a user: {err_msg}')
    return render_template('register.html',form=form)


@app.route('/login/', methods=['GET','POST'])
def login():
    login=LoginForm()
    if login.validate_on_submit():
        usr=User.query.get(login.username.data).first()
        if usr and usr.check_pass_corr(passw=login.password.data):
            login_user(usr)                                               # LOGIN_USER , USER OBJECT IS PASSED IN
            return render_template(url_for(market_page))
        else:
            return 'wrong pass'

    return render_template('login.html',login=login)

@login_required                                                         # LOGIN_REQUIRED ALLOWS LOGGED IN USER TO VIEW PROTECTED PAGES            
@app.route('/transaction/<string:item>/',methods=['GET','POST'])

def transact(item):
    purch=Purch()                                                   # FORM CREATED FOR PURCHASE #
    if purch.validate_on_submit(): #purch.validate_on_submit() here is important because it is used for additional vaidation
                                                                 # behind the scenes. ( ) # request.method == 'POST' is normal
        print(request.form.get('purchased_item'))
        
        item_upd = Item.query.filter_by(name=request.form.get('purchased_item')).first()   # CHECKS IF ITEM OBJECT EXISTS FOR NAME
        if item_upd:                                                                       # CHECKS IF THE ITEM OBJECT IS NONE                              
            if current_user.can_purch(item_upd):                                           # CHECKS IF USER HAS ENOUGH MONEY TO PURCHASE ITEM
                item_upd.owner = current_user.id                                           # logic to purchase item
                current_user.coins = current_user.coins - item_upd.price
                db.session.commit()
                return redirect(url_for('market_page'))
    return render_template('purch.html',purch=purch,item=item)

@app.route('/sell/<item>',methods=['GET','POST'])                                      # ROUTE FOR SELLING
def sell(item):
    sell_form = Sell()
    if sell_form.validate_on_submit():                                                 # CONDITION TRUE WHEN SUBMITED
        item_upd = Item.query.filter_by(name=request.form.get('sold_item')).first()    # FINDS THE * ITEM * OBJECT FOR * ITEM * NAME
        if item_upd:                                                                   # CHECKS IF THE ITEM OBJECT IS NONE     
            if current_user.can_sell(item_upd):                                                # CHECKS IF * USER * HAS * ITEM * OR NOT
                item_upd.sell(current_user)                                            # UPDATES USER DET
                return redirect(url_for('market_page'))
    return render_template('sell.html',item=item,sell=sell_form)

@app.route('/logout',methods=['GET','POST'])
def logout():
    logout_user()
    return redirect(url_for('home_page'))