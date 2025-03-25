import db

def add_recipe(title, ingredient, instruction, user_id):
    sql = """INSERT INTO recipes (title, ingredient, instruction, user_id)
            VALUES (?, ?, ?, ?)"""

    db.execute(sql, [title, ingredient, instruction, user_id])
