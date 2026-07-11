from flask import Flask, request, redirect, render_template

app = Flask(__name__)

import sqlite3
connection=sqlite3.connect("Project.db", check_same_thread=False)
cursor=connection.cursor()


@app.route("/")

def home():

    cursor.execute("""
        SELECT DISTINCT category, subcategory, SUM(amount)
        FROM operations
        GROUP BY category, subcategory
        ORDER BY category
    """)
    operations = cursor.fetchall()

    cursor.execute("""
            SELECT COUNT(*), SUM(amount)
            FROM operations 
            """)
    stats = cursor.fetchone()
    sql_count = stats[0]
    sql_total = stats[1]

    cursor.execute("""
            SELECT category, sum(amount)
            FROM operations
            GROUP BY category
            ORDER BY SUM(amount) DESC
            """)
    categories = cursor.fetchall()


    return render_template('home.html',
                           operations=operations,
                           stats=stats,
                           categories=categories,
                           sql_count=sql_count,
                           sql_total=sql_total
                           )


@app.route("/add_operation")
def add_operation():
    return render_template('add_operation.html')

@app.route("/add", methods=['POST'])
def add():
    category = request.form["category"]
    subcategory = request.form["subcategory"]
    amount = request.form["amount"]

    cursor.execute("""
    INSERT INTO operations
    (category, subcategory, amount)
    VALUES (?, ?, ?)
    """, (category, subcategory, amount))
    connection.commit()

    return redirect("/")

@app.route("/delete")
def delete():


    cursor.execute("""
    SELECT id, category, subcategory, amount
    FROM operations
    """)
    operation_res = cursor.fetchall()

    return render_template('delete.html',
                           operation_res=operation_res
                           )

@app.route("/delete1", methods=['POST'])
def delete1():
    operation_id = request.form["id"]
    cursor.execute("""
    DELETE FROM operations 
    WHERE id = ?
    """, (operation_id, ))
    connection.commit()

    return redirect("/")

@app.route("/update")
def update():


    cursor.execute("""
    SELECT id, category, subcategory, amount
    FROM operations
    """)
    operation_res = cursor.fetchall()

    return render_template(
        'update.html',
        operation_res=operation_res
    )

@app.route("/update1", methods=['POST'])
def update1():
    category = request.form["category"]
    subcategory = request.form["subcategory"]
    amount = request.form["amount"]
    operation_id = request.form["id"]
    cursor.execute("""
    UPDATE operations 
    SET category = ?, subcategory = ?, amount = ?
    WHERE id = ?
    """, (category, subcategory, amount, operation_id ))
    connection.commit()

    return redirect("/")

app.run(port=5002)
