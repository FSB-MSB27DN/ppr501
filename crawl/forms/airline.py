
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class AirlineForm(FlaskForm):
    airline_id = StringField("Airline ID")
    name = StringField("Name", validators=[DataRequired('Name is required'), Length(min=2, message='Name must be greater than 1 character')])
