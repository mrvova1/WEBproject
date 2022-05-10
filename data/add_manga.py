from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, IntegerField, FileField
from wtforms.validators import DataRequired


class AddMangaForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    Release_year = StringField('Release_year', validators=[DataRequired()])
    Title_status = StringField('Title_status', validators=[DataRequired()])
    Author = StringField('Author', validators=[DataRequired()])
    Artist = StringField('Artist', validators=[DataRequired()])
    Interpritator_team = StringField('Interpritator_team', validators=[DataRequired()])
    Number_of_chapters = StringField('Number_of_chapters', validators=[DataRequired()])

    submit = SubmitField('Submit')