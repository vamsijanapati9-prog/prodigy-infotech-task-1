from flask import Flask, render_template, request, redirect, session, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123"

# Temporary database (dictionary)
users = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        if username in users:
            flash("User already exists")
            return redirect('/register')

        users[username] = {
            "password": generate_password_hash(password),
            "role": role
        }
        flash("Registration successful! Please login.")
        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users.get(username)

        if user and check_password_hash(user['password'], password):
            session['user'] = username
            session['role'] = user['role']
            return redirect('/dashboard')
        else:
            flash("Invalid credentials")

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    return render_template('dashboard.html', user=session['user'], role=session['role'])

@app.route('/admin')
def admin():
    if 'role' in session and session['role'] == 'admin':
        return "Welcome Admin!"
    return "Access Denied"

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
