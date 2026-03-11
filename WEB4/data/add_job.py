from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    job = StringField('job', validators=[DataRequired()])
    work_size = StringField('work_size', validators=[DataRequired()])
    collaborators = StringField('collaborators', validators=[DataRequired()])
    start_date = StringField('start_date', validators=[DataRequired()])
    end_date = StringField('end_date', validators=[DataRequired()])
    is_finished = BooleanField('is_finished')
    team_leader = IntegerField('team_leader', validators=[DataRequired()])
    submit = SubmitField('Submit')
