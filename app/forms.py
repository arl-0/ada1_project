from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Length, EqualTo, Regexp, ValidationError, DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4)])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=3, max=20, message="Username must be between 3–20 characters."),
            Regexp("^[A-Za-z0-9_]+$", message="Username can only contain letters, numbers, and underscores.")
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8, max=64, message="Password must be 8–64 characters."),
            Regexp("^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).+$",
                   message="Password must include uppercase, lowercase, and a number.")
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message="Passwords must match.")
        ]
    )
    clearance_level = IntegerField('Clearance Level', validators=[DataRequired()])
    role = SelectField('Role', choices=[('regular', 'Regular User'), ('admin', 'Admin')])
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

    
