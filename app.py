from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///annonces.db'
ALLOWED_EXTENSIONS = ["jpg", "jpeg"]
app.config['MAX_CONTENT_PATH'] = 10000000
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = "static/images/annonces"
db = SQLAlchemy(app)

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


@app.route('/')
def index():
            
    allPosts = Post.query.order_by(Post.date.desc()).all()
    return render_template('index.html', annonces=allPosts)

@app.route('/annonce/create', methods=['GET', 'POST'])
def all_post():

    if request.method == 'POST':

        title           = request.form['title']
        description     = request.form['description']
        mailName        = request.form['mailName']
        mailHost        = request.form['mailHost']
        price           = request.form['price']
        username        = request.form['username']
        asset_condition = request.form['assetCondition']
        image           = request.files['image']

        # if title:
        if description and mailName and mailHost and title and description and price and asset_condition and username:

            mail = '{}@{}'.format(mailName, mailHost)

            newPost = Post(title=title, description=description, mail=mail.lower(), price=price, username=username.lower(), asset_condition=asset_condition)

            db.session.add(newPost)
            db.session.commit()

            if image:
    
                image.save('img_annonce_{}.png'.format(newPost.id))
        
    return redirect('/')

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
                return render_template('index.html', annonces=allPosts)
            
            except UnboundLocalError:
                return render_template('index.html', error='Désolé, nous n\'avons rien trouver qui correspond à la recherche par {} \"{}\"'.format(what_to_search, search))

    return redirect('/')

@app.route('/annonce/delete/<int:id>')
def delete_post(id):

    post = Post.query.get_or_404(id)

    db.session.delete(post)
    db.session.commit()

    return redirect('/')
    
@app.route('/annonce/new')
def new_post():

    return render_template('newPost.html')

@app.route('/annonce/<int:id>')
def annonce(id):
    
    annonce = Post.query.filter_by(id=id).first()

    return render_template('index.html', requestAnnonce=annonce)

if __name__ == '__main__':
    app.run(debug = True)