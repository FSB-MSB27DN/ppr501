from flask import render_template, redirect, url_for
from models.model import AirlineModel
from sqlalchemy import select
from forms.airline import AirlineForm
def airline_list(session):
    airlines = session.execute(select(AirlineModel)).scalars().all()
    
    return render_template('airline_list.html', airlines=airlines)

def airline_add_action(session):
    form = AirlineForm()
    if form.validate_on_submit():
        session.add(AirlineModel(name=form.name.data))
        session.commit()
        return redirect(url_for('route_airline'))
    return render_template('airline_add.html',  form=form)

def airline_edit_action(session, id):
    airline = session.execute(select(AirlineModel).where(AirlineModel.airline_id == id)).scalar_one()
    form = AirlineForm(obj=airline)
    if form.validate_on_submit():
        form.populate_obj(airline)
        session.commit()
        return redirect(url_for('route_airline'))
    return render_template('airline_edit.html', form=form)

def airline_delete_action(session, id):
    airline = session.execute(select(AirlineModel).where(AirlineModel.airline_id == id)).scalar_one()
    session.delete(airline)
    session.commit()
    return redirect(url_for('route_airline'))
