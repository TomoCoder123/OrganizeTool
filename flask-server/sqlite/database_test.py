import sqlite3
conn = sqlite3.connect('recipes.db')
# create a cursor
c = conn.cursor()

# Create a Table
# c.execute("""CREATE TABLE recipes (
#     recipe_name text,
#     time real
# )""") 
# many_recipes = [('recipe5', 6),('recipe6', 4),('recipe7', 5)]
# c.execute("INSERT INTO recipes VALUES ('recipe100', 5 )")

# c.executemany("INSERT INTO recipes VALUES (?, ?)", many_recipes)
c.execute("""UPDATE recipes SET time = 10
          WHERE rowid = 2""")
conn.commit()

c.execute("SELECT rowid, * FROM recipes")
#c.execute("SELECT * FROM recipes WHERE time > 4")


#print(c.fetchone())
# c.fetchmany(3)
#print(c.fetchall()[3])
items = c.fetchall()
#print(items)
for item in items:
    print(item)
print("Command executed successfully...")

# Commit our command
conn.commit()
# Close our connection
conn.close()
