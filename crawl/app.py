from flask import Flask, render_template, redirect, url_for,request
import secrets
import os
from airline import airline_list, airline_add_action, airline_edit_action, airline_delete_action
from aircraft import aircraft_list, aircraft_add_action, aircraft_edit_action, aircraft_delete_action
from flight import flight_list, flight_add_action, flight_edit_action, flight_delete_action
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.model import Base, AirlineModel, AirCraftModel, FlightModel
from forms.login import LoginForm
from sqlalchemy import select

secret_key = secrets.token_hex(16)
app = Flask(__name__)
app.config['SECRET_KEY']=secret_key

# Tạo kết nối với SQLite thông qua SQLAlchemy
engine = create_engine("sqlite:///airline.db")
Session = sessionmaker(bind=engine)
session = Session()

# Tạo bảng trong DB
Base.metadata.create_all(engine)
    
@app.route('/', methods=['GET', 'POST'])
def route_home():

    airlines = session.execute(select(AirlineModel)).scalars().all()
    data = []
    for airline in airlines:
        data_airline = {}
        data_airline['airline_name'] = airline.name
        data_airline['total_aircrafts'] = session.query(AirCraftModel).where(AirCraftModel.airline_id == airline.airline_id).count()
        data_airline['total_flights'] = session.query(FlightModel).where(FlightModel.airline_id == airline.airline_id).count()
        data_airline['total_on_time_flights'] = session.query(FlightModel).where(FlightModel.airline_id == airline.airline_id).filter(FlightModel.status == 'On Time').count()
        data_airline['total_delayed_flights'] = session.query(FlightModel).where(FlightModel.airline_id == airline.airline_id).filter(FlightModel.status == 'Delayed').count()
        data.append(data_airline)
    statistics = {
        'total_aircrafts': session.query(AirCraftModel).count(),
        'total_flights': session.query(FlightModel).count(),
        'total_on_time_flights': session.query(FlightModel).filter(FlightModel.status == 'On Time').count(),
        'total_delayed_flights': session.query(FlightModel).filter(FlightModel.status == 'Delayed').count()
    }
    return render_template('dashboard.html', statistics=statistics, data=data)


@app.route('/login', methods=['GET', 'POST'])
def route_login():
    form = LoginForm()
    error = None

    if form.validate_on_submit():
        if (form.username.data == 'admin' and form.password.data == '123456'):
            return redirect('/')
        else:
            error = "Invalid username or password"
    return render_template('login.html', form=form, error=error)

@app.route('/logout')
def route_logout():
    return render_template('logout.html')


@app.route('/airlines')
def route_airline():
    return airline_list(session)

@app.route('/airline/add', methods=['GET', 'POST'])
def route_airline_add():
    return airline_add_action(session)

@app.route('/airline/edit/<int:id>', methods=['GET', 'POST'])
def route_airline_edit(id):
    return airline_edit_action(session, id)

@app.route('/airline/delete/<int:id>', methods=['GET'])
def route_airline_delete(id):
    return airline_delete_action(session, id)

@app.route('/aircrafts')
def route_aircraft():
    airline_id = request.args.get('airline_id')
    search = request.args.get('search') 
    return aircraft_list(session, airline_id, search)

@app.route('/aircraft/add', methods=['GET', 'POST'])
def route_aircraft_add():
    return aircraft_add_action(session) 

@app.route('/aircraft/edit/<int:id>', methods=['GET', 'POST'])
def route_aircraft_edit(id):
    return aircraft_edit_action(session, id)

@app.route('/aircraft/delete/<int:id>', methods=['GET'])
def route_aircraft_delete(id):
    return aircraft_delete_action(session, id)  

@app.route('/flights')
def route_flight():
    return flight_list(session) 

@app.route('/flight/add', methods=['GET', 'POST'])
def route_flight_add():
    return flight_add_action(session)

@app.route('/flight/edit/<int:id>', methods=['GET', 'POST'])
def route_flight_edit(id):
    return flight_edit_action(session, id)

@app.route('/flight/delete/<int:id>', methods=['GET'])
def route_flight_delete(id):
    return flight_delete_action(session, id)

if __name__ == '__main__':
    app.run(debug=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
