from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

class UpdateForm(FlaskForm):
    rating = StringField(label='Your rating out of 10 e.g. 7.5',validators=[DataRequired()])
    review = StringField(label="Your Review")
    submit = SubmitField(label='Done')

class AddForm(FlaskForm):
    movie = StringField(label="Movie Title",validators=[DataRequired()])
    submit = SubmitField(label="Add movie")