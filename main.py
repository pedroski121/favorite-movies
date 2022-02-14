from flask import render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
import form
import sqlmodel
import searchmovies


app = sqlmodel.app
Bootstrap(app)
db = sqlmodel.db
db.create_all()
search = searchmovies.SearchMovies()

@app.route("/")
def home():
    all_movies = db.session.query(sqlmodel.MovieModel).order_by(
        sqlmodel.MovieModel.rating).all()
    ranking = len(all_movies)

    for movie in all_movies:
        movie.ranking = ranking
        ranking -= 1
    db.session.commit()
    return render_template("index.html", movies=reversed(all_movies))


@app.route('/edit/<movieid>', methods=['GET', 'POST'])
def edit(movieid):
    editform = form.UpdateForm()
    if editform.validate_on_submit():
        user_rating = editform.rating.data
        user_review = editform.review.data
        movie_to_update = sqlmodel.MovieModel.query.get(movieid)
        movie_to_update.rating = user_rating
        movie_to_update.review = user_review
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit.html', updateform=editform)


@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    query = sqlmodel.MovieModel.query.get(id)
    db.session.delete(query)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/add', methods=['GET', 'POST'])
def add():
    addForm = form.AddForm()
    if addForm.validate_on_submit():
        movie_name = addForm.movie.data
        movie_data = search.get_movies(movie_name)
        return render_template('select.html', movies=movie_data['results'])
    return render_template('add.html', form=addForm)


@app.route('/id/<movie_id>', methods=['GET', 'POST'])
def id(movie_id):
    movie_specific = search.get_movie_by_id(movie_id)
    print(movie_specific)
    movie = sqlmodel.MovieModel(
        title=movie_specific['TITLE'],
        description=movie_specific['DESCRIPTION'],
        year=int(movie_specific['YEAR'].split('-')[0]),
        img_url=movie_specific['IMG_URL'],
        rating='',
        ranking=10,
        review=''
    )
    db.session.add(movie)
    db.session.commit()
    id = sqlmodel.MovieModel.query.filter_by(
        title=movie_specific['TITLE']).first().id
    return redirect(url_for('edit', movieid=id))


if __name__ == '__main__':
    app.run(debug=True)
