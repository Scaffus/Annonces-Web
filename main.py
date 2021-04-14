from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class Post(db.Model):

    id          = db.Column(db.Integer, primary_key = True)
    title       = db.Column(db.Text, nullable = False)
    description = db.Column(db.Text, nullable = False)
    mail        = db.Column(db.Text, nullable = False)
    price       = db.Column(db.Text, nullable = False)
    username    = db.Column(db.Text, nullable = False)
    zip_code    = db.Column(db.Text, nullable = False)

    def __repr__(self):
        return 'Post ' + str(self.id)


@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':

        title       = request.form['title']
        description = request.form['description']
        mail        = request.form['mail']
        price       = request.form['price']
        username    = request.form['username']
        zip_code    = request.form['zip_code']

        # if title:
        if description:
            if mail:
                newPost = Post(title=title, description=description, mail=mail, price=price, username=username, zip_code=zip_code)

                db.session.add(newPost)
                db.session.commit()
            else:
                return redirect('/')
            # else:
            #     return redirect('/')
        else:
            return redirect('/')

        
        return redirect('/')
        
    else:

        allPosts = Post.query.order_by(Post.id.desc()).all()
        return render_template('index.html', posts=allPosts)

@app.route('/post/delete/<int:id>')
def delete(id):

    post = Post.query.get_or_404(id)

    db.session.delete(post)
    db.session.commit()

    return redirect('/')
    
@app.route('/newPost')
def new_post():

    return render_template('newPost.html')

if __name__ == '__main__':
    app.run(debug = True)