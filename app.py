from flask import Flask, render_template, request, redirect, url_for, session, logging, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_manager, login_user, login_required, logout_user, current_user, LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '9cb5bead08f09c4c4f70714befb23807e9a25f609fb969cd'
ALLOWED_EXTENSIONS = ["jpg", "jpeg"]
app.config['MAX_CONTENT_PATH'] = 10000000
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = "static/images/annonces"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):

    return User.query.get(int(id))

class Post(db.Model):

    id              = db.Column(db.Integer, primary_key = True)
    title           = db.Column(db.Text, nullable = False)
    description     = db.Column(db.Text, nullable = False)
    mail            = db.Column(db.Text, nullable = False)
    price           = db.Column(db.Text, nullable = False)
    username        = db.Column(db.Text, nullable = False)
    asset_condition = db.Column(db.Text, nullable = False)
    date            = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return '<Annonce: {}>'.format(str(self.id))

class User(db.Model, UserMixin):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    mail    = db.Column(db.String(120))
    password = db.Column(db.String(80))

@app.route('/')
def index():
            
    allPosts = Post.query.order_by(Post.date.desc()).all()
    return render_template('index.html', user=current_user, annonces=allPosts)

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        mail     = request.form['mail']
        password = request.form['password']

        user = User.query.filter_by(mail=mail).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Vous avez été connecté avec succès!', category='success')
                login_user(user, remember=True)
            else:
                flash('Le mot de passe est incorrect.', category='error')
        else:
            flash('L\'addresse email n\'existe pas.')

    return render_template('login.html', user=current_user)

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        mail     = request.form['mail']

        user = User.query.filter_by(mail=mail).first()
        if user:
            flash('L\'addresse email existe déjà.', category='error')

        elif len(mail) < 4:
            flash('L\'addresse mail doit contennir plus de 3 caractères.', category='error')

        elif len(username) < 3:
            flash('Le pseudonyme doit contennir plus de 2 caractères.', category='error')

        elif len(mail) < 8:
            flash('Le mot de passe doit faire au moins 8 caractères.', category='error')

        else:
            newUser = User(username=username, mail=mail, password=generate_password_hash(password, method='sha256'))

            db.session.add(newUser)
            db.session.commit()

            login_user(user, remember=True)

            flash('Compte créé avec succès!', category='success')

        return redirect(url_for('login'))
    return render_template('register.html', user=current_user)

@app.route('/logout')
@login_required
def logout():

    logout_user()

    return redirect('/login')

@app.route('/annonce/create', methods=['GET', 'POST'])
@login_required
def all_post():

    if request.method == 'POST':

        title           = request.form['title']
        description     = request.form['description']
        mail            = request.form['mail']
        price           = request.form['price']
        username        = request.form['username']
        asset_condition = request.form['assetCondition']
        image           = request.files['image']

        if description and mail and title and description and price and asset_condition and username:


            newPost = Post(title=title, description=description, mail=mail.lower(), price=price, username=username.lower(), asset_condition=asset_condition)

            db.session.add(newPost)
            db.session.commit()

            if image:
    
                image.save('img_annonce_{}.png'.format(newPost.id))
        
    return redirect(url_for('index'))

@app.route('/annonce/search', methods=['GET', 'POST'])
def search_post():

    if request.method == 'POST':

        search         = request.form['search']
        what_to_search = request.form['what_to_search']
        
        if search and what_to_search:

            if what_to_search == 'username':
                allPosts = Post.query.filter_by(username=search).all()

            elif what_to_search == 'title':
                allPosts = Post.query.filter_by(title=search).all()

            elif what_to_search == 'price':
                allPosts = Post.query.filter_by(price=search).all()
            
            elif what_to_search == 'mail':
                allPosts = Post.query.filter_by(mail=search).all()

            elif what_to_search == 'asset_condition':
                allPosts = Post.query.filter_by(asset_condition=search).all()
            
            try:
                return render_template('index.html', annonces=allPosts, user=current_user)
            
            except UnboundLocalError:
                return render_template('index.html', error='Désolé, nous n\'avons rien trouver qui correspond à la recherche par {} \"{}\"'.format(what_to_search, search), user=current_user)

    return redirect(url_for('index'))

@app.route('/annonce/delete/<int:id>')
@login_required
def delete_post(id):

    post = Post.query.get_or_404(id)

    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('index'))
    
@app.route('/annonce/new')
@login_required
def new_post():

    return render_template('newPost.html', user=current_user)

@app.route('/annonce/<int:id>')
def annonce(id):
    
    annonce = Post.query.filter_by(id=id).first()

    return render_template('index.html', requestAnnonce=annonce, user=current_user)

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)