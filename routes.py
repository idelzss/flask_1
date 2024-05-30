import os
import requests
from .models import session, Car
from . import app
from flask import render_template, request, redirect, Blueprint
from dotenv import load_dotenv


load_dotenv()

main = Blueprint('main', __name__, template_folder='/templates')
app.register_blueprint(main)

@app.route("/")
def list_cars():
    cars = session.query(Car).all()
    return render_template("cars.html", cars=cars)


@app.route("/car_detail/<int:id>")
def car_detail(id):
    car = session.query(Car).get(id)
    return render_template("car_detail.html", car=car)


@app.route("/car_create", methods=["GET", "POST"])
def create_car():
    if request.method == "POST":
        model_name = request.form["model_name"]
        engine = request.form["engine"]
        type_of_fuel = request.form["type_of_fuel"]

        car = Car(
            model=model_name,
            engine=engine,
            tof=type_of_fuel
        )

        try:
            session.add(car)
            session.commit()
            return redirect("/cars-list")
        except Exception as exc:
            return exc
        finally:
            session.close()
    else:
        return render_template("car_create.html")


@app.route("/car_edit/<int:id>", methods=["GET", "POST"])
def edit_car(id):
    car = session.query(Car).get(id)
    if request.method == "POST":
        model_name = request.form["model_name"]
        engine = request.form["engine"]
        type_of_fuel = request.form["type_of_fuel"]

        car.model_name = model_name
        car.engine = engine
        car.type_of_fuel = type_of_fuel
        session.commit()
        session.close()
        return redirect("/cars-list")
    else:
        return render_template("car_edit.html", car=car)


@app.route("/delete_car/<int:id>")
def delete_car(id):
    car_to_delete = session.query(Car).filter_by(id=id)
    session.delete(car_to_delete)
    session.close()
    return redirect("/cars-list")



@app.route("/exchange", methods=["GET", "POST"])
def exchange():
    if request.method == "POST":
        url = f"https://{os.getenv('API_HOST_RAPID')}/exchange"
        from_value = request.form["from"]
        to_value = request.form["to"]
        count = request.form["count"]
        querystring = {"from": from_value, "to": to_value}
        headers = {
            "X-RapidAPI-Key": os.getenv("API_KEY_RAPID"),
            "X-RapidAPI-Host": os.getenv("API_HOST_RAPID")
        }
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        result = data * int(count)
        return render_template("exchange.html", result=result)
    else:
        return render_template("exchange.html")