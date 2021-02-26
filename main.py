from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
db = SQLAlchemy(app)
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location', validators=[DataRequired()])
    map_url = StringField('Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL()])
    image = StringField('Cafe Image', validators=[DataRequired(), URL()])
    seats = StringField('Number of seats', validators=[DataRequired()])
    coffee = StringField('Coffee Price', validators=[DataRequired()])
    wifi = SelectField('Has wifi?', choices=["✔", "❌"])
    power = SelectField('Has Power Socket?', choices=["✔", "❌"])
    toilet = SelectField('Has Toilet?', choices=["✔", "❌"])
    calls = SelectField('Can take calls?', choices=["✔", "❌"])
    submit = SubmitField('Submit')


class Cafe(db.Model):
    id = id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250))
    coffee_price = db.Column(db.String(250))


db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/cafes")
def cafes():
    all_cafes = db.session.query(Cafe).all()
    return render_template("cafes.html", cafes=all_cafes)


@app.route("/add", methods=["GET", "POST"])
def add():
    add_form = CafeForm()
    if add_form.validate_on_submit():

        def get_yes_or_no(input):
            if input == "❌":
                return False
            else:
                return True

        new_cafe = Cafe(
            name=add_form.cafe.data,
            map_url=add_form.map_url.data,
            img_url=add_form.image.data,
            location=add_form.location.data,
            has_sockets=get_yes_or_no(add_form.power.data),
            has_toilet=get_yes_or_no(add_form.toilet.data),
            has_wifi=get_yes_or_no(add_form.wifi.data),
            can_take_calls=get_yes_or_no(add_form.calls.data),
            seats=add_form.seats.data,
            coffee_price=add_form.coffee.data
        )

        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("cafes"))
    return render_template("add.html", form=add_form)


@app.route("/delete")
def delete():
    cafe_id = request.args.get("id")
    cafe = Cafe.query.filter_by(id=cafe_id).first()
    db.session.delete(cafe)
    db.session.commit()
    return redirect(url_for("cafes"))


@app.route("/edit", methods=["GET", "POST"])
def edit():
    cafe_id = request.args.get("id")
    cafe = db.session.query(Cafe).get(cafe_id)
    edit_form = CafeForm()
    if edit_form.validate_on_submit():

        def get_yes_or_no(input):
            if input == "❌":
                return False
            else:
                return True

        db.session.delete(cafe)
        db.session.commit()

        new_cafe = Cafe(
            id=cafe_id,
            name=edit_form.cafe.data,
            map_url=edit_form.map_url.data,
            img_url=edit_form.image.data,
            location=edit_form.location.data,
            has_sockets=get_yes_or_no(edit_form.power.data),
            has_toilet=get_yes_or_no(edit_form.toilet.data),
            has_wifi=get_yes_or_no(edit_form.wifi.data),
            can_take_calls=get_yes_or_no(edit_form.calls.data),
            seats=edit_form.seats.data,
            coffee_price=edit_form.coffee.data
        )

        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("cafes"))

    return render_template("edit.html", form=edit_form)


if __name__ == "__main__":
    app.run(debug=True)
