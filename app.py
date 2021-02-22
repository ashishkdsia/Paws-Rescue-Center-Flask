from flask import Flask, render_template, abort
from forms import SignUpForm, LoginForm, EditForm
from flask import session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rsgsgsrdthasrhasdrh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///paws.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


# Model for Pets
class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    age = db.Column(db.String)
    bio = db.Column(db.String)
    posted_by = db.Column(db.String, db.ForeignKey('users.id'))


# Model for users
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullName = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    pets = db.relationship('Pet', backref='users')


db.create_all()


# pets = [
#     {"id": 1, "name": "Nelly", "age": "5 weeks",
#      "bio": "I am a tiny kitten rescued by the good people at Paws Rescue Center. I love squeaky toys and cuddles."},
#     {"id": 2, "name": "Yuki", "age": "8 months",
#      "bio": "I am a handsome gentle-cat. I like to dress up in bow ties."},
#     {"id": 3, "name": "Basker", "age": "1 year",
#      "bio": "I love barking. But, I love my friends more."},
#     {"id": 4, "name": "Mr. Furrkins", "age": "5 years", "bio": "Probably napping."},
# ]
#
# users = [
#     {'id': 1, 'fullName': 'Pet Rescue Team',
#      'email': 'team@pawrescue.com', 'password': 'adminpass'}
# ]
#
# pet1 = Pet(name='Nelly', age='5 weeks', bio='I am a tiny kitten rescued by the good people at Paws Rescue Center. I '
#                                             'love squeaky toys and cuddles.')
# pet2 = Pet(name='Yuki', age='8 months', bio="I am a handsome gentle-cat. I like to dress up in bow ties.")
# pet3 = Pet(name='Basker', age='1 year', bio="I love barking. But, I love my friends more.")
# pet4 = Pet(name='Mr. Furrkins', age='5 years', bio="Probably napping.")
#
# db.session.add(pet1)
# db.session.add(pet2)
# db.session.add(pet3)
# db.session.add(pet4)
#
# try:
#     db.session.commit()
# except Exception as e:
#     db.session.rollback()
# finally:
#     db.session.close()


@app.route('/')
def home():
    pets = Pet.query.all()
    return render_template('home.html', pets=pets)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/details/<int:id_no>', methods=['GET', 'POST'])
def details(id_no):
    form = EditForm()
    pet = Pet.query.get(id_no)
    # pet = next((pet for pet in pets if pet['id'] == id_no), None)
    if pet is None:
        abort(404, description='No pet was found with the given ID')
    if form.validate_on_submit():
        pet.name = form.name.data
        pet.age = form.age.data
        pet.bio = form.bio.data
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return render_template('details.html', pet=pet, form=form, message="A Pet with this name already exists!")
    return render_template('details.html', pet=pet, form=form)


@app.route('/delete/<int:id_no>')
def delete_pet(id_no):
    pet = Pet.query.get(id_no)
    if pet is None:
        abort(404, description='No pet was found with the given ID')
    db.session.delete(pet)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('home', _external=True))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        new_user = Users(fullName=form.fullName.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)

        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template('signup.html', form=form,
                                   message="This Email already exists in the system! Please Log in instead.")
        finally:
            db.session.close()
        return render_template('signup.html', message="Successfully Signed Up")
    return render_template('signup.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data, password=form.password.data).first()

        if user is None:
            return render_template('login.html', form=form, message='Wrong Credentials, Please Try Again.')
        else:
            session['user'] = user.id
            return redirect(url_for('home', _schema='https', _external=True))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('home', _external=True))


if __name__ == '__main__':
    app.run(debug=True)
