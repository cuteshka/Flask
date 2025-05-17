from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class DepartAdditionForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    chief = StringField('chief', validators=[DataRequired()])
    members = StringField('members (separated by commas)', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    submit = SubmitField('Confirm')
