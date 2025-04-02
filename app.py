import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
import config
import db
import recipes
import users


app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_recipes = recipes.get_recipes()
    return render_template("index.html", recipes = all_recipes)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    if not username:
        abort(403)
    password1 = request.form["password1"]
    if not password1 or len(password1) < 4:
        abort(403)
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        if not username:
            abort(403)
        password = request.form["password"]
        if not password:
            abort(403)

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")

@app.route("/new_recipe")
def new_recipe():
    require_login()
    classes = recipes.get_all_classes()
    return render_template("new_recipe.html", classes=classes)

@app.route("/create_recipe", methods=["POST"])
def create_recipe():
    require_login()
    title = request.form["title"]
    if not title or len(title) > 80:
        abort(403)
    ingredient = request.form["ingredient"]
    if not ingredient or len(ingredient) > 1000:
        abort(403)
    instruction = request.form["instruction"]
    if not instruction or len(instruction) > 2000:
        abort(403)
    user_id = session["user_id"]

    all_classes = recipes.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))

    recipes.add_recipe(title, ingredient, instruction, user_id, classes)

    return redirect("/")

@app.route("/recipe/<int:recipe_id>")
def show_recipe(recipe_id):
    recipe = recipes.get_recipe(recipe_id)
    if not recipe:
        abort(404)

    classes = recipes.get_classes(recipe_id)
    reviews = recipes.get_reviews(recipe_id)

    return render_template("show_recipe.html", recipe=recipe, classes=classes, reviews=reviews)

@app.route("/edit_recipe/<int:recipe_id>")
def edit_recipe(recipe_id):
    require_login()
    recipe = recipes.get_recipe(recipe_id)
    if not recipe:
        abort(404)
    if recipe["user_id"] != session["user_id"]:
        abort(403)

    all_classes = recipes.get_all_classes()
    classes = {}
    for my_class in all_classes:
        classes[my_class] = ""
    for entry in recipes.get_classes(recipe_id):
        classes[entry["title"]] = entry["value"]

    return render_template("edit_recipe.html", recipe=recipe, classes=classes, all_classes=all_classes)

@app.route("/update_recipe", methods=["POST"])
def update_recipe():
    require_login()
    recipe_id = request.form["recipe_id"]
    recipe = recipes.get_recipe(recipe_id)
    if not recipe:
        abort(404)
    if recipe["user_id"] != session["user_id"]:
        abort(403)

    title = request.form["title"]
    if not title or len(title) > 80:
        abort(403)
    ingredient = request.form["ingredient"]
    if not ingredient or len(ingredient) > 1000:
        abort(403)
    instruction = request.form["instruction"]
    if not instruction or len(instruction) > 2000:
        abort(403)

    all_classes = recipes.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))

    recipes.update_recipe(recipe_id, title, ingredient, instruction, classes)

    return redirect("/recipe/" + str(recipe_id))

@app.route("/remove_recipe/<int:recipe_id>", methods=["GET", "POST"])
def remove_recipe(recipe_id):
    require_login()
    recipe = recipes.get_recipe(recipe_id)
    if not recipe:
        abort(404)
    if recipe["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_recipe.html", recipe=recipe)

    if request.method == "POST":
        if "remove" in request.form:
            recipes.remove_recipe(recipe_id)
            return redirect("/")
        else:
            return redirect("/recipe/" + str(recipe_id))


@app.route("/find_recipe")
def find_recipe():
    query = request.args.get("query")
    if query:
        results = recipes.find_recipes(query)
        return render_template("find_recipe.html", query=query, results=results)
    else:
        query = ""
        results = []
        return render_template("find_recipe.html", query=query, results=results)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    recipes = users.get_recipes(user_id)
    reviews_received = users.get_received_reviews(user_id)
    reviews_given = users.get_given_reviews(user_id)
    return render_template("show_user.html", user=user, recipes=recipes, reviews_received=reviews_received, reviews_given=reviews_given)

@app.route("/create_review", methods=["POST"])
def create_review():
    require_login()

    comment = request.form["comment"]
    if not comment or len(comment) > 500:
        abort(403)
    grade = request.form["grade"]
    if not grade:
        abort(403)
    recipe_id = request.form["recipe_id"]
    recipe = recipes.get_recipe(recipe_id)
    if not recipe:
        abort(403)

    user_id = session["user_id"]

    recipes.add_review(recipe_id, user_id, comment, grade)

    return redirect("/recipe/" + str(recipe_id))

