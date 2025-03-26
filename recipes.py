import db

def add_recipe(title, ingredient, instruction, user_id):
    sql = """INSERT INTO recipes (title, ingredient, instruction, user_id)
            VALUES (?, ?, ?, ?)"""

    db.execute(sql, [title, ingredient, instruction, user_id])

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
    return db.query(sql, [recipe_id])[0]

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
