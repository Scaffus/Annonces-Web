from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///annonces.db'
db = SQLAlchemy(app)

class Post(db.Model):

    id              = db.Column(db.Integer, primary_key = True)
    title           = db.Column(db.Text, nullable = False)
    description     = db.Column(db.Text, nullable = False)
    mail            = db.Column(db.Text, nullable = False)
    price           = db.Column(db.Text, nullable = False)
    username        = db.Column(db.Text, nullable = False)
    asset_condition = db.Column(db.Text, nullable = False)

    def __repr__(self):
        return '<Annonce: {}>'.format(str(self.id))


@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':

        title           = request.form['title']
        description     = request.form['description']
        mailName        = request.form['mailName']
        mailHost        = request.form['mailHost']
        price           = request.form['price']
        username        = request.form['username']
        asset_condition = request.form['assetCondition']

        # if title:
        if description and mailName and mailHost and title and description and price and asset_condition and username:

            mail = '{}@{}'.format(mailName, mailHost)

            newPost = Post(title=title, description=description, mail=mail, price=price, username=username, asset_condition=asset_condition)

            db.session.add(newPost)
            db.session.commit()

        
        return redirect('/')
        
    else:

        allPosts = Post.query.order_by(Post.id.desc()).all()
        return render_template('index.html', annonces=allPosts)

@app.route('/post/delete/<int:id>')
def delete(id):

    post = Post.query.get_or_404(id)

    db.session.delete(post)
    db.session.commit()

    return redirect('/')
    
@app.route('/newPost')
def new_post():

    return render_template('newPost.html')

@app.route('/annonce/<int:id>')
def annonce(id):
    
    annonce = Post.query.filter_by(id=id).first()

    return render_template('index.html', requestAnnonce=annonce)

if __name__ == '__main__':
    app.run(debug = True)