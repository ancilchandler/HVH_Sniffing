from flask import Flask, render_template, redirect, url_for, request, flash, make_response
import base64
import hashlib

app = Flask(__name__)
app.secret_key = "some_secret_key"

# In-memory 'database' using a dictionary
users = {}
users["testuser"] = "testpassword"
users["admin"] = "SuperSeCurePassphrase999"

# Storing the hashed password for target_user
hashed_password = "c9f4b8200faf4114995bd09fdc3def271bdd206b2c223b3967da74e818ecdd0e"
users["target_user"] = hashed_password

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        stored_password = users.get(username)
        if username == "target_user":
            hashed_input_password = hash_password(password)
            if hashed_input_password == stored_password:
                response = make_response(redirect(url_for('protected')))
                cookie_bytes = username.encode("ascii")
                base64_bytes = base64.b64encode(cookie_bytes)
                base64_string = base64_bytes.decode("ascii")
                response.set_cookie('user_id', base64_string, max_age=3600)
                return response
        elif stored_password == password:
            response = make_response(redirect(url_for('protected')))
            cookie_bytes = username.encode("ascii")
            base64_bytes = base64.b64encode(cookie_bytes)
            base64_string = base64_bytes.decode("ascii")
            response.set_cookie('user_id', base64_string, max_age=3600)
            return response
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login')))
    response.delete_cookie('user_id')
    return response

@app.route('/protected')
def protected():
    user_id = request.cookies.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    base64_bytes = user_id.encode("ascii")
    ret_string_bytes = base64.b64decode(base64_bytes)
    new_string = ret_string_bytes.decode("ascii")
    print(new_string)
    return f"Hello {new_string}! Welcome to the protected page."

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
