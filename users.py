from werkzeug.security import generate_password_hash, check_password_hash

import db

def get_user(user_id):
    sql = "SELECT id, username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_recipes(user_id):
    sql = """SELECT id, title FROM recipes
             WHERE user_id = ?"""
    return db.query(sql, [user_id])

def get_received_reviews(user_id):
    sql = """SELECT reviews.id FROM reviews, recipes
            WHERE recipes.id = reviews.recipe_id
            AND recipes.user_id = ?"""
    return db.query(sql, [user_id])

def get_average_grade(user_id):
    sql = """SELECT ROUND(AVG(grade), 1) FROM reviews, recipes
            WHERE recipes.id = reviews.recipe_id
            AND recipes.user_id = ?"""
    result = db.query(sql, [user_id])
    return result[0][0]

def get_given_reviews(user_id):
    sql = "SELECT grade FROM reviews WHERE user_id = ?"
    return db.query(sql, [user_id])

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None

    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    else:
        return None
