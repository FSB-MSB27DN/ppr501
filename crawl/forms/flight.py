
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField
from wtforms.validators import DataRequired

class FlightForm(FlaskForm):
    flight_id = StringField("Flight ID")
    flight_number = StringField("Flight Number", validators=[DataRequired()])
    aircraft_id = SelectField("Aircraft", choices=[], validators=[DataRequired()])
    date = DateField("Date", validators=[DataRequired()], format='%Y-%m-%d')
    from_airport = StringField("From Airport", validators=[DataRequired()])
    to_airport = StringField("To Airport", validators=[DataRequired()])
    scheduled_time_of_departure = StringField("Scheduled Time of Departure", validators=[DataRequired()])
    scheduled_time_of_arrival = StringField("Scheduled Time of Arrival", validators=[DataRequired()])
    actual_time_of_departure = StringField("Actual Time of Departure")
    actual_time_of_arrival = StringField("Actual Time of Arrival")
    status = SelectField("Status", choices=[("-", "-"),("On Time", "On Time"), ("Delayed", "Delayed")], validators=[DataRequired()])

