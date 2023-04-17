
import re
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed,FileField
from wtforms import StringField, PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.fields  import DateField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError,Regexp
from website.models import UserModel
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username =  StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Sign Up')
    remember = BooleanField(label='Remember me')

    def validate_username(self, username):
        if not re.match(r"^[a-zA-Z0-9_]*$", username.data):
            raise ValidationError('only letters, numbers, and underscores are allowed.')
        if UserModel.find_by_username(username.data):
            raise ValidationError('Username used already')
        
    def validate_email(self, email):
        if UserModel.find_by_email(email.data):
            raise ValidationError('Email used already')
        
    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.password.data != self.confirm_password.data:
            self.confirm_password.errors.append("Passwords do not match")
            return False
        return True


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember =  BooleanField('Remember Me')
    submit = SubmitField('Login')

#Account
class Account(FlaskForm):
    new_username = StringField("New Username", validators=[DataRequired(),Length(min=3,max=20)])
    new_email = StringField("New EmailId", validators=[Email(),DataRequired()])
    submit = SubmitField('Update Account')
    
    def validate_username(self,new_username):
        if new_username.data != current_user.username:
            if not re.match(r"^[a-zA-Z0-9_]*$", new_username.data):
                raise ValidationError('only letters, numbers, and underscores are allowed.')
            if UserModel.find_by_username(new_username.data):
                raise ValidationError("Username Already present")
            
    def validate_email(self,new_email):
        if new_email.data != current_user.email:
            if UserModel.find_by_email(new_email.data):
                raise ValidationError("Email Id used already")
            
    def validate_username(self,new_username):
        if new_username.data != current_user.username:
            username = UserModel.find_by_username(new_username.data)
            if username:
                raise ValidationError("Username Already present")

#stocks selector
class Stock(FlaskForm):
    stock_id = StringField("The Stock id you want to explore", validators=[DataRequired(),Length(min=3,max=20)])
    start_date = StringField("Start Date, 20221201 or 2022-12-01", validators=[DataRequired(),Length(min=8,max=10)])
    end_date = StringField("End Date, 20221201 or 2022-12-01", validators=[DataRequired(),Length(min=8,max=10)])
    index = StringField("Index, close, etc", validators=[DataRequired()])
    submit = SubmitField('Start exploring!')

    def validate_username(self,stock_id):
        if UserModel.find_by_stock_id(stock_id.data) == False:
            raise ValidationError("Stock id not exist now!")

     