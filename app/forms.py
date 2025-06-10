from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4)])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4)])
    clearance = SelectField(
        'Clearance Level',
        choices=[(1, 'Level 1'), (2, 'Level 2'), (3, 'Level 3')],
        coerce=int
    )
    submit = SubmitField('Register')

class AssetForm(FlaskForm):
    asset_number = StringField('Asset Number', validators=[InputRequired()])
    title = StringField('Title', validators=[InputRequired()])
    content = TextAreaField('Full Content', validators=[InputRequired()])
    redacted_text = TextAreaField('Redacted Version', validators=[InputRequired()])
    clearance_level = SelectField(
        'Required Clearance Level',
        choices=[(1, 'Level 1'), (2, 'Level 2'), (3, 'Level 3'), (4, 'Level 4'), (5, 'Level 5')],
        coerce=int
    )
    submit = SubmitField('Create Entry')

    