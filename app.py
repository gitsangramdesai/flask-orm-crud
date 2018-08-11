from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class students(db.Model):
   id = db.Column('student_id', db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   city = db.Column(db.String(50))
   addr = db.Column(db.String(200)) 
   pin = db.Column(db.String(10))

   def __init__(self, name, city, addr,pin):
      self.name = name
      self.city = city
      self.addr = addr
      self.pin = pin

@app.route('/')
def show_all():
   return render_template('show_all.html', students = students.query.all() )

@app.route('/delete')
def delete():
   sname = request.args.get('name')
   s = students.query.filter_by(name=sname).first()
   db.session.delete(s)
   db.session.commit()
   return redirect("/", code=302)

@app.route('/edit', methods = ['GET', 'POST'])
def edit():
      if request.method == 'POST':
            name = request.form['name']
            s = students.query.filter_by(name=name).first()
            s.city = request.form['city']
            s.addr = request.form['addr']
            s.pin = request.form['pin']
          
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
      else:
            sname = request.args.get('name')
            s = students.query.filter_by(name=sname).first()
            return render_template('edit.html',data = s)



@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['name'] or not request.form['city'] or not request.form['addr']:
         flash('Please enter all the fields', 'error')
      else:
         student = students(request.form['name'], request.form['city'],request.form['addr'], request.form['pin'])
         
         db.session.add(student)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('show_all'))

   s = students('','','','')
   return render_template('new.html',data=s)

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)
