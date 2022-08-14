from flask_app import app
from flask import render_template, redirect, request, flash, abort, session

from datetime import datetime

# Importing Models
from flask_app.models.painting import Painting
from flask_app.models.user import User

@app.route("/paintings")
def paintings():
    if session.get("user_id"):
        user_ = User.get_by_id({"id": session["user_id"]})
        paintings = Painting.get_all()
        return render_template("dashboard.html", user_=user_, paintings=paintings)
    return redirect("/")

@app.route("/painting/<id>")
def view_painting(id):
    if session.get("user_id"):
        painting = Painting.get_by_id({"id": id})
        if painting:
            return render_template("view_painting.html", user_info=session, painting=painting)
        abort(404)
    return redirect('/')



@app.route("/add_painting", methods=["POST", "GET"])
def add_painting(): 
    if session.get("user_id"):
        if request.method == "POST":
            invalid = False

            user_id = session.get("user_id")

            data = request.form

            if not data["title"]:
                invalid = True
                flash("Title cannot be empty", "title")

            if not data["description"]:
                invalid = True
                flash("Description cannot be empty", "description")
            elif len(data["description"]) < 10:
                invalid = True
                flash("Description sould be at least 10 characters long", "description")


            if not data["price"]:
                invalid = True
                flash("Price is mandatory!", "price")
            else:
                try:
                    x = float(data["price"])
                    if x < 1:
                        invalid = True
                        flash("Price should be greater than 0", "price")                
                except Exception as e:
                    invalid = True
                    flash("Price should be a number", "price")                
               

            if not invalid:
                Painting.create({**request.form, "user_id": user_id})
                return redirect("/paintings")

        return render_template(
            "add_painting.html", user_info=session, data=request.form
        )

    return redirect("/")



@app.route("/painting/<id>/edit", methods=["GET", "POST"])
def edit_painting(id):
    if session.get("user_id"):
        painting = Painting.get_by_id({"id": id})
        if painting:
            if painting.user.id == session["user_id"]:
                if request.method == "POST":
                    invalid = False

                    data = request.form

                    if not data["title"]:
                        invalid = True
                        flash("Title cannot be empty", "title")
          
                    if not data["description"]:
                        invalid = True
                        flash("Description cannot be empty", "description")
                    elif len(data["description"]) < 10:
                        invalid = True
                        flash("Description sould be at least 10 characters long", "description")

                    if not data["price"]:
                        invalid = True
                        flash("Price is mandatory!", "price")
                    try:
                        x = float(data["price"])
                        if x < 1:
                            invalid = True
                            flash("Price should be greater than 0", "price")                
                    except Exception as e:
                        invalid = True
                        flash("Price should be a number", "price")                

                    if not invalid:
                        Painting.edit(
                            {**request.form, "id": painting.id}
                        )
                        return redirect("/paintings")

                    return render_template(
                        "edit_painting.html", user_info=session, data={**request.form, "id": painting.id}
                    )

                return render_template(
                        "edit_painting.html", user_info=session, data=painting.__dict__
                )
            abort(403)
        abort(404)
    return redirect("/")


@app.route("/painting/<id>/delete")
def delete_painting(id):
    if session.get("user_id"):
        painting = Painting.get_by_id({"id": id})
        if painting:
            if painting.user.id == session["user_id"]:
                Painting.delete({"id": painting.id})
                return redirect("/paintings")
            abort(403)
        abort(404)
    return redirect("/")


