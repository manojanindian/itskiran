
from flask import Flask, url_for, render_template, request, redirect, url_for, session, flash
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
  return render_template("home.html", img_url=img_url)



# Admin Login page
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    user = AdminUser.query.filter_by(username=username, password=password).first()
    if user:
      session['admin_logged_in'] = True
      return redirect(url_for('admin_dashboard'))
    else:
      flash('Invalid credentials', 'danger')
  return render_template('admin_login.html')




# Admin Dashboard page (empty)
@app.route('/admin/dashboard')
def admin_dashboard():
  if not session.get('admin_logged_in'):
    return redirect(url_for('admin_login'))
  return render_template('admin_dashboard.html')


# Admin Logout route
@app.route('/admin/logout')
def admin_logout():
  session.pop('admin_logged_in', None)
  flash('Logged out successfully.', 'info')
  return redirect(url_for('admin_login'))



# Redirect to home if page not found
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('home'))

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)


# #2f8da3
