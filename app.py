from flask import Flask, redirect, render_template, session, flash
from models import db, connect_db, User, Feedback
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterUserForm, LoginForm, FeedbackForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretsecrets'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.debug = True
toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def homepage():
    """Renders the hompage for the website"""
    return render_template ('homepage.html')

@app.route('/register', methods=['GET', 'POST'])
def show_register_form():
    """Handles the Registration form and creates a new user"""
    form = RegisterUserForm()

    if form.validate_on_submit():
       username = form.username.data
       password = form.password.data
       email = form.email.data
       first_name = form.first_name.data
       last_name = form.last_name.data

       user = User.register(username, password, email, first_name, last_name)

       session['username'] = username
       db.session.add(user)
       db.session.commit()

       return redirect(f'/users/{username}')

    else:
        return render_template('register_form.html', form = form )
    
@app.route('/users/<username>')
def show_user_information(username):
    """Shows the details of a user"""
    if session['username'] == username:
        user = User.query.filter_by(username = username).first()
        user_feedback = Feedback.query.filter_by(username = username).all()
        return render_template('user_details.html', user = user, user_feedback = user_feedback )
    
    else:
        flash('You do not have permission to view requested page')
        return redirect('/')
    

@app.route('/login', methods=['GET', 'POST'])
def log_in_form():
    """Handles the login form and authenticates user"""
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            return redirect(f'/users/{username}')
        
        else: 
            form.username.errors = ['Bad/ name/password']
            return redirect('/login')

    else:
        return render_template('login_form.html',  form=form)
        

@app.route('/logout')
def logout():
    """Logs a user out of the website and clears session cookies"""

    if session['username']:
        
        session.pop('username')

        return redirect('/')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def create_feedback_form(username):
    """Handles the feeback form and submits a users feedback"""
    form = FeedbackForm()

    if session['username'] == username:
    
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            username = f'{username}'

            new_feedback = Feedback(title=title, content=content, username=username)

            db.session.add(new_feedback)
            db.session.commit()

            return redirect(f'/users/{username}')

        else:
            user = User.query.filter_by(username = username).first()

            return render_template('create_feedback_form.html', form = form, user = user)
    else:
        flash('You do not have permissions to access that route')
        return redirect('/')

@app.route('/feedback/<int:id>/update', methods=['GET','POST'])
def update_feedback(id):
    """Handles the feedback form and updates a the feedback post of a user"""
    form = FeedbackForm()
    feedback = Feedback.query.get(id)
    user = feedback.user

    if session['username'] == feedback.user.username:


        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
        
            db.session.commit()


            return redirect(f'/users/{user.username}')
        
        else:
            return render_template('edit_feedback_form.html', form = form, user=user, feedback = feedback)
    
    else:
        flash('You do not have permissions to access that route')
        return redirect('/')

@app.route('/feedback/<int:id>/delete', methods=['POST'])
def delete_feedback(id):
    """Deletes the feedback of a user"""
    username = Feedback.query.get(id).user.username
    feedback = Feedback.query.get(id)

    if session['username'] == feedback.user.username:

        db.session.delete(feedback)
        db.session.commit()

        return redirect(f'/users/{username}')
    
    else: 
        flash('You do not have permissions to access that route')
        return redirect('/')