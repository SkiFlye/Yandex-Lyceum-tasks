from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    job = StringField('Job Title', validators=[DataRequired()])
    work_size = IntegerField('Work Duration (hours)', validators=[DataRequired()])
    collaborators = StringField('Collaborators (IDs with comma)', validators=[DataRequired()])
    is_finished = BooleanField('Is finished?')
    category = SelectMultipleField('Categories', coerce=int)
    submit = SubmitField('Submit')