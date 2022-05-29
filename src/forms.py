from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Length,EqualTo,Email,DataRequired
from src import User

class RegisterForm(FlaskForm):
    def validate_username(self,usernametochk):
        user=User.query.filter_by(name=usernametochk.data).first()
        if user:
            raise ValidationErr("naw")

    def validate_email(self,emailtochk):
        email = User.query.filter_by(email=emailtochk.data).first()
        if email:
            raise ValidationErr("newww")

    username = StringField(label='username')#,validators=[Length(min=2,max=30),DataRequired()])
    email = StringField(label='email')#,validators=[Email(),DataRequired()])
    password1=PasswordField(label="password")#,validators=[Length(min=6),DataRequired()])
    pass2=PasswordField(label="confirm password")#,validators=[EqualTo(password1)])
    submit = SubmitField(label='submit')

class LoginForm(FlaskForm):
    username = StringField(label='username')
    password1=PasswordField(label="password")
    submit = SubmitField(label='submit')

class Purch(FlaskForm):
    submit =SubmitField(label="submit")

class Sell(FlaskForm):
    submit =SubmitField(label="submit")

class LogoutForm(FlaskForm):
    submit =SubmitField(label="submit")