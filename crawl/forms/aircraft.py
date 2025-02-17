
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired

class AircraftForm(FlaskForm):
    aircraft_id = StringField("Aircraft ID")
    name = StringField("Name", validators=[DataRequired()])
    type = StringField("Type", validators=[DataRequired()])
    airline_id = SelectField("Airline", choices=[], validators=[DataRequired()])
