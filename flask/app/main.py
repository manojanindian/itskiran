
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


# Jwellery table
from datetime import datetime
class Jwellery(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  image_path = db.Column(db.String(255), nullable=False)
  uploaded_date = db.Column(db.DateTime, default=datetime.utcnow)
  price = db.Column(db.Float, nullable=True)
  quantity = db.Column(db.Integer, nullable=False, default=0)

# Create tables and default admin user

import sqlite3
def add_column_if_not_exists(db_path, table, column, col_type, default):
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()
  cursor.execute(f"PRAGMA table_info({table})")
  columns = [info[1] for info in cursor.fetchall()]
  if column not in columns:
    cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type} NOT NULL DEFAULT {default}")
    conn.commit()
  conn.close()

with app.app_context():
  db.create_all()
  # Add 'quantity' column to jwellery table if missing
  add_column_if_not_exists(DB_PATH, 'jwellery', 'quantity', 'INTEGER', 0)
  if not AdminUser.query.filter_by(username='admin').first():
    db.session.add(AdminUser(username='admin', password='admin'))
    db.session.commit()


# Flask-Admin setup
admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')
admin.add_view(ModelView(AdminUser, db.session))
admin.add_view(ModelView(Jwellery, db.session))



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
# Admin Dashboard page (empty)

# Admin Dashboard page (empty)
@app.route('/admin/dashboard')
def admin_dashboard():
  if not session.get('admin_logged_in'):
    return redirect(url_for('admin_login'))
  return render_template('admin_dashboard.html')

# Admin Jwellery page

@app.route('/admin/jwellery', methods=['GET', 'POST'])
def admin_jwellery():
  if not session.get('admin_logged_in'):
    return redirect(url_for('admin_login'))
  if request.method == 'POST':
    # Handle price and quantity update for existing image
    update_id = request.form.get('update_id')
    update_price = request.form.get('update_price')
    update_quantity = request.form.get('update_quantity')
    if update_id and (update_price is not None or update_quantity is not None):
      try:
        price_val = float(update_price) if update_price else None
      except ValueError:
        price_val = None
      try:
        quantity_val = int(update_quantity) if update_quantity else 0
      except ValueError:
        quantity_val = 0
      img_obj = Jwellery.query.get(int(update_id))
      if img_obj:
        if update_price is not None:
          img_obj.price = price_val
        img_obj.quantity = quantity_val
        db.session.commit()
        flash('Price/Quantity updated!', 'success')
        return redirect(url_for('admin_jwellery'))
    # Handle new image upload
    images = request.files.getlist('images')
    price = request.form.get('price')
    quantity = request.form.get('quantity')
    price_val = float(price) if price else None
    try:
      quantity_val = int(quantity) if quantity else 0
    except ValueError:
      quantity_val = 0
    for img in images:
      if img and img.filename:
        filename = f"jwellery/{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}_{img.filename}"
        save_path = os.path.join(app.root_path, 'static', filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        img.save(save_path)
        db.session.add(Jwellery(image_path=filename, price=price_val, quantity=quantity_val))
    if images:
      db.session.commit()
      flash('Images uploaded successfully!', 'success')
      return redirect(url_for('admin_jwellery'))
  images = Jwellery.query.order_by(Jwellery.uploaded_date.desc()).all()
  return render_template('admin_jwellery.html', images=images)


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
