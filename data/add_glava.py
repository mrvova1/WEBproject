from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, IntegerField, FileField
from wtforms.validators import DataRequired


class AddGlavaForm(FlaskForm):
    id = IntegerField('id', validators=[DataRequired()])

    submit = SubmitField('Submit')