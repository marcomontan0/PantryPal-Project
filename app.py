from flask import Flask, render_template, request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pantry.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @property
    def status(self):
        days_left = (self.expiration_date - date.today()).days
        if days_left < 0:
            return 'Expired'
        elif days_left <= 3:
            return 'Expiring Soon'
        else:
            return 'Fresh'
    @property
    def days_left(self):
        return (self.expiration_date - date.today()).days

@app.route('/')
def index():
    return render_template('base.html')
                           
@app.route('/pantry')
def pantry():
    items = Item.query.all()
    return render_template('Pantry.html', items=items)

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        expiration = datetime.strptime(request.form['expiration_date'], '%Y-%m-%d').date()

        new_item = Item(name=name, expiration_date=expiration)
        db.session.add(new_item)
        db.session.commit()

        return redirect('/pantry')

    return render_template('add_item.html')

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    item = Item.query.get(item_id)

    db.session.delete(item)
    db.session.commit()

    return redirect('/pantry')

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    
    if request.method == 'POST':
        item.name = request.form['name']
        item.expiration_date = datetime.strptime(request.form['expiration_date'], '%Y-%m-%d').date()
        db.session.commit()
        return redirect('/pantry')
    
    return render_template('edit_item.html', item=item)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
