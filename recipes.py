import db

def add_recipe(title, ingredient, instruction, user_id, classes):
    sql = """INSERT INTO recipes (title, ingredient, instruction, user_id)
            VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, ingredient, instruction, user_id])

    recipe_id = db.last_insert_id()

    sql = """INSERT INTO recipe_classes (recipe_id, title, value)
            VALUES (?, ?, ?)"""
    for class_title, class_value in classes:
        db.execute(sql, [recipe_id, class_title, class_value])

def get_classes(recipe_id):
    sql = """SELECT title, value FROM recipe_classes
            WHERE recipe_id = ?"""
    return db.query(sql, [recipe_id])

def get_recipes():
    sql = "SELECT id, title FROM recipes"
    return db.query(sql)

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)

    return classes

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

def update_recipe(recipe_id, title, ingredient, instruction, classes):
    sql = """UPDATE recipes SET title = ?,
                                ingredient = ?,
                                instruction = ?
                            WHERE id = ?"""

    db.execute(sql, [title, ingredient, instruction, recipe_id])

    sql = "DELETE FROM recipe_classes WHERE recipe_id = ?"
    db.execute(sql, [recipe_id])

    sql = """INSERT INTO recipe_classes (recipe_id, title, value)
            VALUES (?, ?, ?)"""
    for class_title, class_value in classes:
        db.execute(sql, [recipe_id, class_title, class_value])

def remove_recipe(recipe_id):
    sql = "DELETE FROM recipe_classes WHERE recipe_id = ?"
    db.execute(sql, [recipe_id])
    sql = "DELETE FROM reviews WHERE recipe_id = ?"
    db.execute(sql, [recipe_id])
    sql = "DELETE FROM recipes WHERE id = ?"
    db.execute(sql, [recipe_id])

def find_recipes(query):
    sql = """SELECT id, title
            FROM recipes
            WHERE title LIKE ? OR ingredient LIKE ?"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])

def add_review(recipe_id, user_id, comment, grade):
    sql = """INSERT INTO reviews (recipe_id, user_id, comment, grade)
            VALUES (?, ?, ?, ?)"""
    db.execute(sql, [recipe_id, user_id, comment, grade])

def get_reviews(recipe_id):
    sql = """SELECT r.comment, r.grade, u.id user_id, u.username
            FROM reviews r, users u
            WHERE r.recipe_id = ? AND r.user_id = u.id
            ORDER BY r.id"""
    return db.query(sql, [recipe_id])
