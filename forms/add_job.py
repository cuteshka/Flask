from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobAdditionForm(FlaskForm):
    job = StringField('Job title', validators=[DataRequired()])
    teamleader = IntegerField('Teamleader id', validators=[DataRequired()])
    work_size = IntegerField('Work Size', validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    is_finished = BooleanField('is job finished')
    submit = SubmitField('Submit')
