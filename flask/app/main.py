
from flask import Flask, url_for, render_template_string, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os

app = Flask(__name__)

app.secret_key = 'supersecretkey'  # Change this in production

DB_PATH = os.path.join(os.path.dirname(__file__), "sqlite", "app.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Admin table
class AdminUser(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)

# Create tables and default admin user
with app.app_context():
  #db.create_all()
  if not AdminUser.query.filter_by(username='admin').first():
    db.session.add(AdminUser(username='admin', password='admin'))
    db.session.commit()

# Flask-Admin setup
admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')
admin.add_view(ModelView(AdminUser, db.session))




# Home page
@app.route("/")
def home():
    img_url = url_for("static", filename="itskiran-color.jpg")
    return f"""
        <html>
          <head>
            <style>
              body {{
                background-color: #2f8da3;
                font-family: Arial, sans-serif;
                text-align: center;
                margin-top: 50px;
              }}
              img {{
                border-radius: 10px;
                box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
              }}
              h1 {{
                color: white;
              }}
            </style>
          </head>
          <body>
            <h1>coming soon...</h1>
            <img src="{img_url}" alt="ItsKiran Image" width="400">
            <br><br>
            <a href='/login' style='color:white;'>Admin Login</a>
          </body>
        </html>
    """

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = AdminUser.query.filter_by(username=username, password=password).first()
        if user:
            session['admin_logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template_string('''
        <html><head><title>Login</title></head><body style="background:#2f8da3;text-align:center;">
        <h2 style="color:white;">Admin Login</h2>
        <form method="post">
            <input name="username" placeholder="Username"><br><br>
            <input name="password" type="password" placeholder="Password"><br><br>
            <button type="submit">Login</button>
        </form>
        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            {% for category, message in messages %}
              <div style="color:red;">{{ message }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}
        </body></html>
    ''')


# Dashboard page (empty)
@app.route('/dashboard')
def dashboard():
  if not session.get('admin_logged_in'):
    return redirect(url_for('login'))
  return render_template_string('''
    <h1 style="color:#2f8da3;text-align:center;">Dashboard (empty)</h1>
    <div style="text-align:center;margin-top:20px;">
      <a href="/logout">Logout</a>
    </div>
  ''')

# Logout route
@app.route('/logout')
def logout():
  session.pop('admin_logged_in', None)
  flash('Logged out successfully.', 'info')
  return redirect(url_for('login'))


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)


# #2f8da3
