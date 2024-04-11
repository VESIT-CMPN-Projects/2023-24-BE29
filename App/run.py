from flask import Flask, render_template, redirect, request
import os
import sys
# parent_dir = os.path.abspath('..')
# sys.path.append(parent_dir)
from ...MSD_Dir.App import integrate

from werkzeug.utils import secure_filename
# from utils.integrate import execute_models
# from pymongo import MongoClient

app = Flask(__name__)


@app.route("/complainForm", methods=["POST", "GET"])
def complain_form():
    if request.method == "POST":
        owner_name = request.form["ownerName"]
        vehicle_no = request.form["registrationNo"]
        vehicle_color = request.form["carColor"]
        vehicle_model = request.form["carModel"]
        vehicle_image = ""

        try:
            imageFile = request.files["carImage"]
            if imageFile:
                filename = secure_filename(imageFile.filename)
                imageFile.save(
                    os.path.join(
                        "App/images",
                        filename,
                    )
                )
                print("file saved successfully")
        except Exception as e:
            print(e)

        print(f"owner_name: {owner_name}")
        print(f"vehicle_no: {vehicle_no}")
        print(f"vehicle_color: {vehicle_color}")
        print(f"vehicle_model: {vehicle_model}")
        print(f"vehicle_image: {vehicle_image}")
        integrate.execute_models(vehicle_no,vehicle_color,vehicle_model)
        return redirect("/home")

    else:
        return redirect("/")


@app.route("/home")
def home():
    return render_template("dashboard.html")


@app.route("/")
def hello_world():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
