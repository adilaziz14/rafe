from flask import Flask, render_template, request, redirect, session
import urllib.parse

app = Flask(__name__)
app.secret_key = 'mysecretkey'

admin_username = 'abc'
admin_password = '123'

non_admin_username = 'def'
non_admin_password = '456'

ADMIN_URL = "https://console.rafay.dev/#/login"
# + urllib.parse.quote('aadil@13')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']

        if user_type == 'admin' and username == admin_username and password == admin_password:
            session['user_type'] = 'admin'
            return redirect(ADMIN_URL)
        elif user_type == 'non_admin' and username == non_admin_username and password == non_admin_password:
            session['user_type'] = 'non_admin'
            return redirect('/non_admin_dashboard')
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')


@app.route('/non_admin_dashboard')
def non_admin_dashboard():
    if session.get('user_type') != 'non_admin':
        return redirect('/')
    return render_template('non_admin_dashboard.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='127.0.0.1')
