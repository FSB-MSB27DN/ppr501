from flask import render_template, redirect, url_for
from models.model import  AirlineModel, FlightModel, AirCraftModel
from sqlalchemy import select
from forms.flight import FlightForm
from datetime import datetime


def flight_list(session):
    stmt = select(FlightModel)
    flights = session.execute(stmt).scalars().all()
    # print('flights', flights[0].__dict__)
    return render_template('flight_list.html', flights=flights)

def flight_add_action(session):
    form = FlightForm()
    form.aircraft_id.choices = [(aircraft.aircraft_id, aircraft.name) for aircraft in session.execute(select(AirCraftModel)).scalars().all()]
    if form.validate_on_submit():
        new_flight = FlightModel(
            flight_number=form.flight_number.data, 
            aircraft_id=form.aircraft_id.data, 
            date=form.date.data, 
            from_airport=form.from_airport.data, 
            to_airport=form.to_airport.data, 
            scheduled_time_of_departure=form.scheduled_time_of_departure.data, 
            scheduled_time_of_arrival=form.scheduled_time_of_arrival.data, 
            actual_time_of_departure=form.actual_time_of_departure.data,
            actual_time_of_arrival=form.actual_time_of_arrival.data,
            status=form.status.data
            )
        session.add(new_flight)
        session.commit()
        return redirect(url_for('route_flight'))
    return render_template('flight_add.html',  form=form)

def flight_edit_action(session, id):
    flight = session.execute(select(FlightModel).where(FlightModel.flight_id == id)).scalar_one()
    form = FlightForm(obj=flight)
    form.aircraft_id.choices = [(aircraft.aircraft_id, aircraft.name) for aircraft in session.execute(select(AirCraftModel)).scalars().all()]
    if form.validate_on_submit():
        form.populate_obj(flight)
        session.commit()
        return redirect(url_for('route_flight'))
    return render_template('flight_edit.html', form=form)

def flight_delete_action(session, id):
    flight = session.execute(select(FlightModel).where(FlightModel.flight_id == id)).scalar_one()
    session.delete(flight)
    session.commit()
    return redirect(url_for('route_flight'))