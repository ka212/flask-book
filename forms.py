from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    author = StringField('Author', validators=[DataRequired(), Length(min=2, max=20)])
    published_date = DateField('Published Date', validators=[DataRequired()])
    isbn = IntegerField('ISBN', validators=[DataRequired()])
    pages = IntegerField('Pages', validators=[DataRequired()])
    language = StringField('Language', validators=[DataRequired(), Length(min=2, max=20)])
    publisher = StringField('publisher', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Add')
