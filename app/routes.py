from flask import Blueprint, render_template

pages = Blueprint("pages", __name__, template_folder="templates")


@pages.route("/")
def home():
    return render_template("home.html", title="JA - Estética")


@pages.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html", title="JA - Estética | Login")