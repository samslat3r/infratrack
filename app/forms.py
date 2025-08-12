from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, IPAddress

class HostForm(FlaskForm):
    hostname = StringField('Hostname', validators=[DataRequired()])
    ip_address = StringField('IP Address', validators=[DataRequired(), IPAddress()])
    os = StringField('Operating System')
    tags = StringField('Tags (Comma-separated)')
    submit = SubmitField('Save')
    
class TaskForm(FlaskForm):
    host_id = SelectField('Host', coerce=int, validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Save')

class ChangeForm(FlaskForm):
    host_id = SelectField('Host', coerce=int, validators=[DataRequired()])
    summary = StringField('Summary', validators=[DataRequired()])
    submit = SubmitField('Save')
