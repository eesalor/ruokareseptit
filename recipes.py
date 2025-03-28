import db

def add_recipe(title, ingredient, instruction, user_id, classes):
    sql = """INSERT INTO recipes (title, ingredient, instruction, user_id)
            VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, ingredient, instruction, user_id])

    recipe_id = db.last_insert_id()

    sql = "INSERT INTO recipe_classes (recipe_id, title, value) VALUES (?, ?, ?)"
    for title in classes:
        for value in classes[title]:
            db.execute(sql, [recipe_id, title, value])

def get_classes(recipe_id):
    sql = """SELECT title, value FROM recipe_classes
            WHERE recipe_id = ?"""
    return db.query(sql, [recipe_id])

def get_recipes():
    sql = "SELECT id, title FROM recipes"

    return db.query(sql)

def get_recipe(recipe_id):
    sql = """SELECT recipes.id,
                    recipes.title,
                    recipes.ingredient,
                    recipes.instruction,
                    users.id user_id,
                    users.username
            FROM recipes, users
            WHERE recipes.user_id = users.id AND recipes.id = ?"""
    result = db.query(sql, [recipe_id])
    return result[0] if result else None

def update_recipe(recipe_id, title, ingredient, instruction):
    sql = """UPDATE recipes SET title = ?,
                                ingredient = ?,
                                instruction = ?
                            WHERE id = ?"""

    db.execute(sql, [title, ingredient, instruction, recipe_id])

def remove_recipe(recipe_id):
    sql = "DELETE FROM recipes WHERE id = ?"
    db.execute(sql, [recipe_id])

def find_recipes(query):
    sql = """SELECT id, title
            FROM recipes
            WHERE title LIKE ? OR ingredient LIKE ?"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])
