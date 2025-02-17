from flask import render_template, redirect, url_for
from models.model import AirCraftModel, AirlineModel
from sqlalchemy import select
from forms.aircraft import AircraftForm

def aircraft_list(session, airline_id = None, search = None):
    stmt = select(AirCraftModel).join(AirCraftModel.airline)
    if airline_id:
        stmt = stmt.where(AirCraftModel.airline_id == airline_id)
    if search:
        stmt = stmt.where(AirCraftModel.name.like(f'%{search}%'))
    aircrafts = session.execute(stmt).scalars().all()
    airlines = session.execute(select(AirlineModel)).scalars().all()
    return render_template('aircraft_list.html', aircrafts=aircrafts, airlines=airlines)

def aircraft_add_action(session):
    form = AircraftForm()
    form.airline_id.choices = [(airline.airline_id, airline.name) for airline in session.execute(select(AirlineModel)).scalars().all()]
    print(form.airline_id.data)
    if form.validate_on_submit():
        session.add(AirCraftModel(name=form.name.data, type=form.type.data, airline_id=form.airline_id.data))
        session.commit()
        return redirect(url_for('route_aircraft'))
    return render_template('aircraft_add.html',  form=form)

def aircraft_edit_action(session, id):
    aircraft = session.execute(select(AirCraftModel).where(AirCraftModel.aircraft_id == id)).scalar_one()
    form = AircraftForm(obj=aircraft)
    form.airline_id.choices = [(airline.airline_id, airline.name) for airline in session.execute(select(AirlineModel)).scalars().all()]
    if form.validate_on_submit():
        form.populate_obj(aircraft)
        session.commit()
        return redirect(url_for('route_aircraft'))
    return render_template('aircraft_edit.html', form=form)

def aircraft_delete_action(session, id):
    aircraft = session.execute(select(AirCraftModel).where(AirCraftModel.aircraft_id == id)).scalar_one()
    session.delete(aircraft)
    session.commit()
    return redirect(url_for('route_aircraft'))