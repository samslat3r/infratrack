from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, IPAddress, Length, Regexp

class HostForm(FlaskForm):
    # RFC Compliant hostname validation
    hostname = StringField('Hostname', validators=[
        DataRequired(), 
        Length(min=1, max=63),
        Regexp(r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?$', 
               message="Invalid hostname format")
    ])
    ip_address = StringField('IP Address', validators=[DataRequired(), IPAddress()])
    os = StringField('Operating System', validators=[Length(max=64)])
    tags = StringField('Tags (Comma-separated)', validators=[Length(max=255)])
    submit = SubmitField('Save')
    
class TaskForm(FlaskForm):
    host_id = SelectField('Host', coerce=int, validators=[DataRequired()])
    description = TextAreaField('Description', validators=[
        DataRequired(), 
        Length(min=1, max=255)
    ])
    submit = SubmitField('Save')

class ChangeForm(FlaskForm):
    host_id = SelectField('Host', coerce=int, validators=[DataRequired()])
    summary = StringField('Summary', validators=[
        DataRequired(), 
        Length(min=1, max=255)
    ])
    submit = SubmitField('Save')
