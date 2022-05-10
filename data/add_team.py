from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class AddTeamForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    Line_up = StringField('Line_up', validators=[DataRequired()])
    Permissions = StringField('Permissions', validators=[DataRequired()])

    submit = SubmitField('Submit')
