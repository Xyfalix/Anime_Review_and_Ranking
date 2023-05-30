from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, TextAreaField
from wtforms.validators import DataRequired, NumberRange
from search_anime import search_anime, search_by_id

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# Create Database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///top10anime.db"
db = SQLAlchemy(app)


# setup Anime class for database config
class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.Text)
    img_url = db.Column(db.Text, nullable=False)


class RatingForm(FlaskForm):
    change_rating = FloatField('Your rating out of 10. E.g 7.5', validators=[NumberRange(min=1, max=10)],
                               render_kw={"style": "width: 500px"})
    review = TextAreaField('Enter your review here', validators=[DataRequired()],
                           render_kw={"rows": 5, "style": "width: 500px"})
    submit = SubmitField("Done")


class AddAnime(FlaskForm):
    new_anime = StringField('Anime Title', validators=[DataRequired()])
    submit = SubmitField("Add Anime")


with app.app_context():
    db.create_all()
    db.session.commit()


@app.route("/")
def home():
    # This creates a SQLAlchemy query object that selects all rows from the Anime table.
    query = db.session.query(Anime)
    # This sorts the results of the query object in ascending order of the rating column
    # and stores the sorted list of Anime objects in ordered_anime
    ordered_anime = query.order_by(Anime.rating).all()
    # sets the initial rank to the length of the ordered_anime list
    rank = len(ordered_anime)
    # loops through each Anime object in ordered_anime and sets its ranking attribute to the current rank value,
    # then decrements the rank value by 1
    for anime in ordered_anime:
        anime.ranking = rank
        rank -= 1
    return render_template("index.html", all_anime=ordered_anime)

@app.route("/add", methods=['GET', 'POST'])
def add_movie():
    form = AddAnime()
    if form.validate_on_submit():
        search_results = search_anime(form.new_anime.data)
        return render_template("select.html", search_results=search_results)
    return render_template("add.html", form=form)

@app.route("/edit/<int:database_id>", methods=['GET', 'POST'])
def edit_rating(database_id):
    form = RatingForm()
    anime = Anime.query.get(database_id)
    if form.validate_on_submit():
        anime.rating = float(form.change_rating.data)
        anime.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", anime=anime, form=form)


@app.route('/delete/<int:database_id>')
def delete(database_id):
    anime = Anime.query.get(database_id)
    if anime:
        db.session.delete(anime)
        db.session.commit()
        print('Anime deleted successfully')
    else:
        print('Anime not found')
    return redirect(url_for('home'))


@app.route('/select/<int:anime_id>')
def select_anime(anime_id):
    anime = search_by_id(anime_id)
    # update the database with the new entry
    new_anime = Anime(
        title=anime['title']['romaji'],
        year=anime['startDate']['year'],
        description=anime['description'],
        img_url=anime['coverImage']['extraLarge']
    )
    db.session.add(new_anime)
    db.session.commit()
    database_id = new_anime.id
    return redirect(url_for('edit_rating', database_id=database_id))


if __name__ == '__main__':
    app.run(debug=True)

