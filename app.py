from flask import Flask, render_template, request
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
        expiration = request.form['expiration_date']

        new_item = Item(
            name=name,
            expiration_date=datetime.strptime(expiration, '%Y-%m-%d')
        )

        db.session.add(new_item)
        db.session.commit()

        return redirect('/pantry')

    return render_template('add_item.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
