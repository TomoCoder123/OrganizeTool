import sqlite3
import sys
import os

def connect_to_db():
    """
    Establish a connection to the SQLite database.

    This function locates the 'recipe_table.db' file in the same directory as the 
    current script and establishes a connection to it.

    Returns:
        sqlite3.Connection: An active connection object to the SQLite database.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    db = os.path.join(path, 'recipe_table.db')    
    conn = sqlite3.connect(db)
    return conn



def create_color_table():
    """
    Create the 'color_table' in the SQLite database. Currently, color table is not being used.

    This function connects to the SQLite database and attempts to create a table named 
    'color_table' with two columns:
        - block_name (text): The name of the block (Starting, Preparing, etc.), which must be unique.
        - color (text): The color associated with the block.

    If the table creation is successful, a success message is printed. If it fails, 
    an error message is printed.

    Exceptions:
        If an error occurs during table creation, the exception is caught and 
        an error message is printed.

    The database connection is closed in the 'finally' block, ensuring that it is 
    always closed after the operation is complete.
    """
    try:
        conn = connect_to_db()
        conn.execute(
            '''
            CREATE TABLE color_table (
                block_name text UNIQUE,
                color text
            );
        '''
        )
        conn.commit()
        print("Color table created successfully")
    except:
        print("Color table creation failed")
    finally:
        conn.close()

def create_calendar_table():
    """
    Create the 'calendar_table' in the SQLite database. The table contains 
    information on the blocks that will be shown on the calendar, so adding/removing,
    aborting, or downing processes all reflect in calendar, where edits and rows are linked
    through furnace_id.

    This function connects to the SQLite database and attempts to create a table named 
    'calendar_table' with the following columns:
        - furnace_id (text): Identifier for the furnace, which references 'primary_id' 
          in the 'furnaces_table'.
        - block (text): Identifier for the block, which references 'block_name' 
          in the 'color_table'.
        - sequence (real): Represents the sequence index for scheduling.
        - end_time (real): Represents the length of the recipe
    """
    try:
        conn = connect_to_db()
        conn.execute(
            '''
            CREATE TABLE calendar_table (
                furnace_id text,
                block text,
                sequence real,
                end_time real,
                FOREIGN KEY (furnace_id) REFERENCES furnaces_table (primary_id),
                FOREIGN KEY (block) REFERENCES color_table (block_name)
            );
        '''
        )
        conn.commit()
        print("Calendar table created successfully")
    except Exception as e:
        print(f"block table creation failed: {e}")
    finally:
        conn.close()
def create_blockname_table():
    """
    Create the 'blockname_table' in the SQLite database. The blockname table contains 
    the information for each recipe before any in-row modifications are made to the 
    recipe.

    This function connects to the SQLite database and attempts to create a table named 
    'blockname_table' with the following columns:
        - recipe_key (text): A reference key for the recipe, which references 'recipe_name'
          in the 'recipe_table'.
        - block (text): Identifier for the block, which references 'block_name' 
          in the 'color_table'.
        - sequence (real): Represents the sequence number for this block in the recipe.
    """
    try:
        conn = connect_to_db()
        conn.execute(
            '''
            CREATE TABLE blockname_table (
                recipe_key text,
                block text,
                sequence real,
                FOREIGN KEY (recipe_key) REFERENCES recipe_table (recipe_name),
                FOREIGN KEY (block) REFERENCES color_table (block_name)
            );
        '''
        )
        conn.commit()
        print("Block table created successfully")
    except Exception as e:
        print(f"block table creation failed: {e}")
    finally:
        conn.close()
def create_db_table():
    """
    Create the 'recipe_table' in the SQLite database. This table contains all the
    recipes, their names, and their lengths.

    This table includes the following columns:
        - recipe_id (INTEGER PRIMARY KEY NOT NULL): A unique identifier for each recipe.
        - recipe_name (text): The name of the recipe, which must be unique.
        - time (real): Represents the length of the recipe.
    """
    try:
        conn = connect_to_db()
        
        conn.execute('''
            CREATE TABLE recipe_table (
                recipe_id INTEGER PRIMARY KEY NOT NULL,
                recipe_name text UNIQUE,
                time real
            );
        ''')
        conn.commit()
        print("Recipe table created successfully")
    except:
        print("Recipe table creation failed - Maybe table")
    finally:
        conn.close()

def create_down_table():
    """
    Create the 'down_table' in the SQLite database. Down reasons correspond to a color in the color table

    This table includes the following column:
        - down_name (text): A down reason that has a reference to 'block_name' in the 'color_table'.
    """
    try: 
        conn = connect_to_db()
        conn.execute('''
                CREATE TABLE down_table (
                    down_name text,
                    FOREIGN KEY (down_name) REFERENCES color_table (block_name) 
                     );
                     ''')
        conn.commit()
        print("down_table created successfully")
    except Exception as e:
        print(f"Down table creation failed - Maybe table {e}")
    finally:
        conn.close()

def create_furnace_recipe_table():
    """
    Create the 'furnace_recipe_table' in the SQLite database. This is a lookup table
    with a one to one connection between furnace and recipe.

    This table includes the following columns:
        - furnace (text UNIQUE): The name of the furnace, which must be unique.
        - recipe (text): A reference to 'recipe_name' in the 'recipe_table'.
    """
    try: 
        conn = connect_to_db()
        conn.execute('''
                CREATE TABLE furnace_recipe_table (
                    furnace text UNIQUE,
                    recipe text,
                    FOREIGN KEY (recipe) REFERENCES recipe_table (recipe_name) 
                     );
                     ''')
        conn.commit()
        print("furnace_recipe_table created successfully")
    except Exception as e:
        print(f"Furnace Recipe table creation failed - {e}")
    finally:
        conn.close()
    
def create_furnace_table():
    """
    Create the 'furnaces_table' in the SQLite database.

    This table includes the following columns:
        - primary_id (INTEGER PRIMARY KEY NOT NULL): A unique identifier for each furnace entry.
        - furnace_name (text): The name of the furnace.
        - start_time (DATE): The start time associated with the furnace.
        - recipe_key (text): A reference to 'recipe_name' in the 'recipe_table'.
    """
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE furnaces_table (
                primary_id INTEGER PRIMARY KEY NOT NULL,
                furnace_name text,
                start_time DATE,
                recipe_key text,
                FOREIGN KEY (recipe_key) REFERENCES recipe_table (recipe_name)
            );
        ''')
        conn.commit()
        print("Furnace table created successfully")
    except Exception as e:
        print(f"Furnace table creation failed - Maybe table{e}")
    finally:
        conn.close()



def create_recipe(recipe):
    """
    Add a new recipe to the 'recipe_table' in the SQLite database.

    This function inserts a new recipe into the 'recipe_table' with the provided
    recipe name and time. After successfully inserting the recipe, it retrieves 
    the newly added recipe by its ID and returns it.

    Args:
        recipe (dict): A dictionary containing the recipe details. Expected keys are:
            - 'recipe_name' (str): The name of the recipe.
            - 'time' (float): The time associated with the recipe.

    Returns:
        dict: A dictionary representing the newly added recipe, or an empty dictionary 
        if an error occurred.

    Exceptions:
        If an error occurs during the insertion, the transaction is rolled back and 
        an error message is printed.

    The database connection is closed after the operation is complete.
    """
    added_recipe = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        # print(recipe['time'])
        cur.execute("INSERT INTO recipe_table (recipe_name, time) VALUES (?, ?)", (recipe['recipe_name'], recipe['time']))
        conn.commit()
        added_recipe = read_recipe_by_id(cur.lastrowid)
        print_database()
    except Exception as e:
        print(f"An error has occurred while creating recipe: {e}")
        conn.rollback()
    finally:
        conn.close()
    return added_recipe
def create_furnace_recipe(furnace_recipe):
    """
    Add a new entry to the 'furnace_recipe_table' in the SQLite database.

    This function inserts a new record into the 'furnace_recipe_table' with the provided
    furnace name and recipe key. After successfully inserting the record, it prints the
    current state of the database.

    Args:
        furnace_recipe (dict): A dictionary containing the furnace recipe details. Expected keys are:
            - 'furnace_name' (str): The name of the furnace.
            - 'recipe_key' (str): The key representing the associated recipe.

    Exceptions:
        If an error occurs during the insertion, the transaction is rolled back and 
        an error message is printed.

    The database connection is closed after the operation is complete.
    """
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        # print(recipe['time'])
        cur.execute("INSERT INTO furnace_recipe_table (furnace, recipe ) VALUES (?, ?)", (furnace_recipe['furnace_name'], furnace_recipe['recipe_key']))
        conn.commit()
        print_database()
    except Exception as e:
        print(f"An error has occurred while creating recipe: {e}")
        conn.rollback()
    finally:
        conn.close()
    return
def create_color(color):
    """
    Add a new color entry to the 'color_table' in the SQLite database.

    This function inserts a new record into the 'color_table' with the provided
    block name and color. After successfully inserting the record, it commits the transaction.

    Args:
        color (dict): A dictionary containing the color details. Expected keys are:
            - 'block_name' (str): The name of the block.
            - 'color' (str): The color associated with the block.

    Exceptions:
        If an error occurs during the insertion, the transaction is rolled back and 
        an error message is printed.

    The database connection is closed after the operation is complete.
    """
    added_color = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        # print(recipe['time'])
        cur.execute("INSERT INTO color_table (block_name, color) VALUES (?, ?)", (color['block_name'], color['color']))
        conn.commit()
    except Exception as e:
        print(f"An error has occurred while creating color: {e}")
        conn.rollback()
    finally:
        conn.close()
def create_down(down):
    """
    Add a new entry to the 'down_table' in the SQLite database.

    This function inserts a new record into the 'down_table' with the provided
    down block name. After successfully inserting the record, it commits the transaction.

    Args:
        down (dict): A dictionary containing the down block details. Expected key:
            - 'down_name' (str): The name of the down block.

    Exceptions:
        If an error occurs during the insertion, the transaction is rolled back and 
        an error message is printed.

    The database connection is closed after the operation is complete.
    """
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        # print(recipe['time'])
        cur.execute("INSERT INTO down_table (down_name) VALUES (?)", (down['down_name'],))
        conn.commit()
    except Exception as e:
        print(f"An error has occurred while creating down_block: {e}")
        conn.rollback()
    finally:
        conn.close()

def create_block(blocks):
    """
    Add multiple block entries to the 'blockname_table' in the SQLite database. Essentially adds all the blocks 
    for a recipe.

    This function inserts multiple records into the 'blockname_table' using the provided
    list of block details. Each entry contains the recipe key, block name, and sequence.
    Foreign key constraints are enforced.

    Args:
        blocks (list of dict): A list of dictionaries, each containing the block details. 
        Each dictionary should have the following keys:
            - 'recipe_key' (str): The key representing the associated recipe.
            - 'block' (str): The name of the block.
            - 'sequence' (float): The sequence number for this block.

    Exceptions:
        If an error occurs during the insertion, the transaction is rolled back and 
        an error message is printed.

    The database connection is closed after the operation is complete.
    """
    # added_furnace = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        # print(recipe['time'])
        cur.execute("PRAGMA foreign_keys=ON")
        
        for i in range(len(blocks)):
            print(blocks[i])
            cur.execute("INSERT INTO blockname_table (recipe_key, block, sequence) VALUES (?, ?, ?)", (blocks[i]['recipe_key'], blocks[i]['block'], blocks[i]['sequence']))
            conn.commit()
       
    except Exception as e:
        print(f"An error has occurred while creating blocks: {e}")
        conn.rollback()
    finally:
        conn.close()
def create_furnace(furnace):
    """
    Add a new furnace entry to the 'furnaces_table' in the SQLite database.

    This function inserts a new record into the 'furnaces_table' with the provided
    furnace details, including the furnace name, associated recipe key, and start time.
    Foreign key constraints are enforced.

    Args:
        furnace (dict): A dictionary containing the furnace details. Expected keys:
            - 'furnace_name' (str): The name of the furnace.
            - 'recipe_key' (str): The key representing the associated recipe.
            - 'start_time' (str): The start time associated with the furnace.
    """
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys=ON")

        cur.execute("INSERT INTO furnaces_table (furnace_name, recipe_key, start_time) VALUES (?, ?, ?)", (furnace['furnace_name'], furnace['recipe_key'], furnace['start_time']))
        conn.commit()
    except Exception as e:
        print(f"An error has occurred while creating furnace: {e}")
        conn.rollback()
    finally:
        conn.close()
def create_calendar(calendars, start, furnace_name):
    """
    Add calendar entries to the 'calendar_table' in the SQLite database.

    This function inserts multiple records into the 'calendar_table' based on the provided
    list of calendar entries, the start time, and the furnace name, basically inserting the default
    recipe in block format. It retrieves the furnace and recipe details from the database to
      calculate the end time for each calendar entry.

    Args:
        calendars (list of dict): A list of dictionaries, each containing the calendar entry details.
        Each dictionary should have the following keys:
            - 'block' (str): The name of the block.
            - 'sequence' (float): The sequence number for this block.
        start (str): The start time associated with the furnace.
        furnace_name (str): The name of the furnace.
    """
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys=ON")
        print("entering loop")
        for i in range(len(calendars)):
            cur.execute("SELECT * FROM furnaces_table WHERE start_time =  ? AND furnace_name = ?", (start, furnace_name))
            row = cur.fetchone()
            print("row")
            print(row)
            id = row[0]
            recipe = row[3]
            cur.execute("SELECT * FROM recipe_table WHERE recipe_name =  ?", (recipe,))
            recipe_row = cur.fetchone()
            time = recipe_row[2]
            cur.execute("INSERT INTO calendar_table (furnace_id, block, sequence, end_time) VALUES (?, ?, ?, ?)", (id, calendars[i]['block'], calendars[i]['sequence'], time))
        conn.commit()
        # added_recipe = read_recipe_by_id(cur.lastrowid)
    except Exception as e:
        print(f"An error has occurred while creating calendar: {e}")
        conn.rollback()
    finally:
        conn.close()
def create_empty_calendar(calendars, furnace):
    """
    Add empty calendar entries to the 'calendar_table' in the SQLite database. This function is used 
    when the start time is not known yet. 

    This function inserts multiple records into the 'calendar_table' based on the provided
    list of calendar entries and furnace details. It retrieves the furnace and associated
    recipe details from the database to calculate the end time for each calendar entry.

    Args:
        calendars (list of dict): A list of dictionaries, each containing the calendar entry details.
        Each dictionary should have the following keys:
            - 'block' (str): The name of the block.
            - 'sequence' (float): The sequence number for this block.
        furnace (dict): A dictionary containing the furnace details. Expected key:
            - 'furnace_name' (str): The name of the furnace.

    Exceptions:
        If an error occurs during the insertion, the transaction is rolled back and 
        an error message is printed.

    The database connection is closed after the operation is complete.
    """
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys=ON")
        for i in range(len(calendars)):
            cur.execute("SELECT * FROM furnaces_table WHERE furnace_name = ?", ( furnace['furnace_name'],))

            row = cur.fetchone()
            print("row")
            print(row)
          
            id = row[0]
            recipe = row[3]
            cur.execute("SELECT * FROM recipe_table WHERE recipe_name =  ?", (recipe,))
            recipe_row = cur.fetchone()
            time = recipe_row[2]
            cur.execute("INSERT INTO calendar_table (furnace_id, block, sequence, end_time) VALUES (?, ?, ?, ?)", (id, calendars[i]['block'], calendars[i]['sequence'], time))
        conn.commit()
        # added_recipe = read_recipe_by_id(cur.lastrowid)
    except Exception as e:
        print(f"An error has occurred while creating empty calendar: {e}")
        conn.rollback()
    finally:
        conn.close()
def read_recipes():
    """
    Retrieve all recipes from the 'recipe_table' in the SQLite database. Used by the GET api call.

    This function queries the 'recipe_table' and retrieves all the recipe records. Each
    record is represented as a dictionary with the following keys:
        - 'recipe_id' (int): The unique identifier for the recipe.
        - 'recipe_name' (str): The name of the recipe.
        - 'time' (float): The time associated with the recipe.

    Returns:
        list of dict: A list of dictionaries representing the recipes. If an error occurs,
        an empty list is returned.
    
    Exceptions:
        If an error occurs during the query, an empty list is returned.
    """
    recipes = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM recipe_table")
        rows = cur.fetchall()
        for i in rows:
            recipe = {}
            recipe["recipe_id"] = i["recipe_id"]
            recipe["recipe_name"] = i["recipe_name"]
            recipe["time"] = i["time"]
            recipes.append(recipe)
    except Exception as e:
        recipes = []
    return recipes

def read_blocks():
    """
    Retrieve all blocks from the 'blockname_table' in the SQLite database.

    This function queries the 'blockname_table' and retrieves all the block records. 
    Each record is represented as a dictionary with the following keys:
        - 'recipe_key' (str): The key representing the associated recipe.
        - 'block' (str): The name of the block.
        - 'sequence' (float): The sequence number for the block.

    Returns:
        list of dict: A list of dictionaries representing the blocks. If an error occurs,
        an empty list is returned.
    
    Exceptions:
        If an error occurs during the query, an error message is printed and an empty 
        list is returned.
    """
    blocks = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM blockname_table")
        rows = cur.fetchall()
        for i in rows:
            block = {}
            block["recipe_key"] = i["recipe_key"]
            block["block"] = i["block"]
            block["sequence"] = i["sequence"]
            blocks.append(block)
    except Exception as e:
        print(f"Error while reading blocks: {e}")
        blocks = []
    return blocks
def read_colors():
    """
    Retrieve all colors from the 'color_table' in the SQLite database.

    This function queries the 'color_table' and retrieves all the color records. 
    Each record is represented as a dictionary with the following keys:
        - 'block_name' (str): The name of the block.
        - 'color' (str): The color associated with the block.

    Returns:
        list of dict: A list of dictionaries representing the colors. If an error occurs,
        an empty list is returned.
    
    Exceptions:
        If an error occurs during the query, an error message is printed and an empty 
        list is returned.
    """
    colors = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM color_table")
        rows = cur.fetchall()
        for i in rows:
            color = {}
            color["block_name"] = i["block_name"]
            color["color"] = i["color"]
            colors.append(color)
    except Exception as e:
        print(f"Error while reading colors {e}")
        colors = []
    return colors
def read_down():
    """
    Retrieve all entries from the 'down_table' in the SQLite database.

    This function queries the 'down_table' and retrieves all the down records. 
    Each record is represented as a dictionary with the following key:
        - 'down_name' (str): The name of the down reason.

    Returns:
        list of dict: A list of dictionaries representing the down entries. If an error occurs,
        an empty list is returned.
    
    Exceptions:
        If an error occurs during the query, an error message is printed and an empty 
        list is returned.
    """
    downs = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM down_table")
        rows = cur.fetchall()
        for i in rows:
            down = {}
            down["down_name"] = i["down_name"]
            downs.append(down)
    except Exception as e:
        print(f"Error while reading downreasons {e}")
        downs = []
    return downs
def read_calendar():
    """
    Retrieve all calendar entries from the 'calendar_table' in the SQLite database.

    This function queries the 'calendar_table' and retrieves all the calendar records. 
    Each record is represented as a dictionary with the following keys:
        - 'furnace_id' (int): The ID of the furnace associated with the calendar entry.
        - 'block' (str): The name of the block associated with the calendar entry.
        - 'sequence' (float): The sequence number for the calendar entry.
        - 'end_time' (float): The end time for the calendar entry.

    Returns:
        list of dict: A list of dictionaries representing the calendar entries. 
        If an error occurs, an empty list is returned.

    Exceptions:
        If an error occurs during the query, an error message is printed, and an empty 
        list is returned.
    """
    calendar_items = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM calendar_table")
        rows = cur.fetchall()
        for i in rows:
            calendar = {}
            calendar["furnace_id"] = i["furnace_id"]
            calendar["block"] = i["block"]
            calendar["sequence"] = i["sequence"]
            calendar["end_time"] = i["end_time"]

            calendar_items.append(calendar)
    except Exception as e:
        print(f"Error while reading calendar {e}")
        calendar_items = []
    return calendar_items
def read_furnaces():
    """
    Retrieve all furnaces from the 'furnaces_table' in the SQLite database.

    This function queries the 'furnaces_table' and retrieves all the furnace records.
    Each record is represented as a dictionary with the following keys:
        - 'primary_id' (int): The unique identifier for the furnace entry.
        - 'furnace_name' (str): The name of the furnace.
        - 'recipe_key' (str): The key representing the associated recipe.
        - 'start_time' (str): The start time associated with the furnace.

    Returns:
        list of dict: A list of dictionaries representing the furnaces. If an error occurs,
        an empty list is returned.

    Exceptions:
        If an error occurs during the query, an empty list is returned.
    """
    furnaces = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM furnaces_table")
        rows = cur.fetchall()
        for i in rows:
            furnace = {}
            furnace["primary_id"] = i["primary_id"]
            furnace["furnace_name"] = i["furnace_name"]
            furnace["recipe_key"] = i["recipe_key"]
            furnace["start_time"] = i["start_time"]
            furnaces.append(furnace)
    except Exception as e:
        furnaces = []
    return furnaces
def read_furnace_recipes():
    """
    Retrieve all furnace recipe entries from the 'furnace_recipe_table' lookup table in the SQLite database.

    This function queries the 'furnace_recipe_table' and retrieves all the furnace recipe records.
    Each record is represented as a dictionary with the following keys:
        - 'furnace' (str): The name of the furnace.
        - 'recipe' (str): The name of the associated recipe.

    Returns:
        list of dict: A list of dictionaries representing the furnace recipe entries. 
        If an error occurs, an empty list is returned.

    Exceptions:
        If an error occurs during the query, an empty list is returned.
    """
    furnace_recipes = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM furnace_recipe_table")
        rows = cur.fetchall()
        for i in rows:
            furnace_recipe = {}
            furnace_recipe["furnace"] = i["furnace"]
            furnace_recipe["recipe"] = i["recipe"]
        
            furnace_recipes.append(furnace_recipe)
    except Exception as e:
        furnace_recipes = []
    return furnace_recipes

def read_recipe_by_id(recipe_id):
    """
    Retrieve a specific recipe by its ID from the 'recipe_table' in the SQLite database. Not being used

    This function queries the 'recipe_table' and retrieves the recipe record corresponding to 
    the given recipe ID. The record is represented as a dictionary with the following keys:
        - 'recipe_id' (int): The unique identifier for the recipe.
        - 'recipe_name' (str): The name of the recipe.
        - 'time' (float): The time associated with the recipe.

    Args:
        recipe_id (int): The ID of the recipe to retrieve.

    Returns:
        dict: A dictionary representing the recipe. If an error occurs, an empty dictionary is returned.

    Exceptions:
        If an error occurs during the query, an error message is printed and an empty dictionary is returned.
    """
    recipe = {}
    # furnacebase()
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        #furnacebase()
        cur.execute("SELECT * FROM recipe_table WHERE recipe_id = ?", (recipe_id,))
        row = cur.fetchone()
        recipe["recipe_id"] = row["recipe_id"]
        recipe["recipe_name"] = row["recipe_name"]
        recipe["time"] = row["time"]
        print("Successfully read")
    except Exception as e:
        print(f"failed to read recipe by id: {e}")
        recipe = {}
    return recipe
def read_furnace_by_id(primary_id):
    """
    Retrieve a specific furnace by its ID from the 'furnaces_table' in the SQLite database.

    This function queries the 'furnaces_table' and retrieves the furnace record corresponding to 
    the given primary ID. The record is represented as a dictionary with the following keys:
        - 'primary_id' (int): The unique identifier for the furnace.
        - 'furnace_name' (str): The name of the furnace.
        - 'start_time' (str): The start time associated with the furnace.

    Args:
        primary_id (int): The ID of the furnace to retrieve.

    Returns:
        dict: A dictionary representing the furnace. If an error occurs, an empty dictionary is returned.

    Exceptions:
        If an error occurs during the query, an error message is printed and an empty dictionary is returned.
    """
    furnace = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM furnaces_table WHERE primary_id = ?", (primary_id,))
        row = cur.fetchone()
        furnace["primary_id"] = row["primary_id"]
        furnace["recipe_name"] = row["furnace_name"]
        furnace["start_time"] = row["start_time"]
        print("Successfully read")
    except Exception as e:
        print(f"failed to read furnace by id: {e}")
        furnace = {}
    return furnace
def update_calendar(number, state, id, action):
    """
    Update or insert entries in the 'calendar_table' in the SQLite database.

    This function updates the `end_time` and `sequence` fields of existing entries in the
    'calendar_table' for the specified `furnace_id`. Depending on the `action` parameter,
    the function either modifies existing records or inserts new ones.

    Args:
        number (int): The value to add to the `sequence` or `end_time` fields.
        state (str): The state of the block to be updated.
        id (int): The ID of the furnace for which the calendar entries are to be updated.
        action (str): The action to perform. Can be "addremove", "Down", or other values like "Aborted".

    Behavior:
        - If `action` is "addremove", the function updates existing rows, modifying the `end_time`
          and `sequence` based on the provided `number`.
        - If `action` contains "Down", a new entry is inserted with the block set to the action name.
        - Otherwise, a new entry is inserted with the block set to "Aborted".
    """
    try:

        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM calendar_table WHERE furnace_id = ?", (id,))
        rows = cur.fetchall()
        end_time = rows[0][3]

        print("rows: ")
        print(rows)
        print(action)
        if(action == "addremove"):
            updated = False
            
            for index, row in enumerate(rows):
                print(row)
                block = row[1]
                if (updated == False):
                    if (block == state):
                        cur.execute("UPDATE calendar_table SET end_time = ? WHERE block = ? AND furnace_id = ?", ( row[3] + int(number), state, id))

                        updated = True
                    else:

                        print("hasn't reached yet")
                        print(row[3]+ int(number))
                        cur.execute("UPDATE calendar_table SET end_time = ? WHERE block = ? AND furnace_id = ?", ( row[3] + int(number), row[1], id))

                else:
                    cur.execute("UPDATE calendar_table SET sequence = ?,  end_time = ? WHERE block = ? AND furnace_id = ?", (int(number) + row[2] , row[3] + int(number), row[1], id))
        elif("Down" in action):
            cur.execute("INSERT INTO calendar_table (furnace_id, block, sequence, end_time) VALUES (?, ?, ?, ?)", (id, action, number, end_time))

        else:
            cur.execute("INSERT INTO calendar_table (furnace_id, block, sequence, end_time) VALUES (?, ?, ?, ?)", (id, "Aborted", number, end_time))
        conn.commit()
    except Exception as e:
        print(f"failed to update calendar: {e}")
        conn.rollback()
    finally:
        conn.close()
def update_recipe(recipe):
    """
    Update an existing recipe in the 'recipe_table' and associated entries in the 'blockname_table' and 'furnaces_table' in the SQLite database.

    This function updates the details of a recipe in the 'recipe_table' based on the provided recipe dictionary.
    It also removes related entries from the 'blockname_table' and updates references to the recipe in the 'furnaces_table'.

    Args:
        recipe (dict): A dictionary containing the updated recipe details. Expected keys:
            - 'recipe_id' (int): The unique identifier of the recipe to update.
            - 'recipe_name' (str): The updated name of the recipe.
            - 'time' (float): The updated time associated with the recipe.

    Behavior:
        - The function first deletes the related entries from the 'blockname_table' based on the old recipe name.
        - It updates the recipe name and time in the 'recipe_table'.
        - It updates any related entries in the 'furnaces_table' that reference the old recipe name.
        - Finally, it commits the changes and retrieves the updated recipe.

    Returns:
        dict: A dictionary representing the updated recipe. If an error occurs, an empty dictionary is returned.
    """
    updated_recipe = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT recipe_name FROM recipe_table WHERE recipe_id = ?", (recipe['recipe_id'],))
        old_recipe_name = cur.fetchone()[0]  # Fetch the first result
        cur.execute("DELETE FROM blockname_table WHERE recipe_key = ?", (old_recipe_name,))

        cur.execute("UPDATE recipe_table SET recipe_name = ?, time = ? WHERE recipe_id = ? ", (recipe['recipe_name'], recipe['time'], recipe['recipe_id']))
        cur.execute("SELECT * FROM furnaces_table WHERE recipe_key = ?", (recipe['recipe_name'],))
        rows = cur.fetchall()
        cur.execute("UPDATE furnaces_table SET recipe_key = ? WHERE recipe_key = ? ", ( recipe['recipe_name'], old_recipe_name))
        conn.commit()
        updated_recipe = read_recipe_by_id(recipe["recipe_id"])
    except Exception as e:
        print(f"failed to update recipe: {e}")
        conn.rollback()
        updated_recipe = {}
    finally:
        conn.close()
def update_furnace_recipe(furnaceRecipe, oldName):
    print(furnaceRecipe)
    try:
        conn = connect_to_db()
        cur = conn.cursor()
    
        cur.execute("""UPDATE furnace_recipe_table SET furnace = ?, recipe = ? WHERE furnace = ? """, (furnaceRecipe['furnace'], furnaceRecipe['recipe'], oldName))

        conn.commit()
    except Exception as e:
        print(f"failed to update furnace_recipe: {e}")

        conn.rollback()
        #updated_furnace = {}
    finally:
        conn.close()



def update_furnace(furnace):
    """
    Update an existing entry in the 'furnace_recipe_table' in the SQLite database.

    This function updates the furnace name and associated recipe in the 'furnace_recipe_table' based on the provided
    new furnace and recipe details. The update is performed on the entry that matches the old furnace name.

    Args:
        furnaceRecipe (dict): A dictionary containing the updated furnace recipe details. Expected keys:
            - 'furnace' (str): The updated name of the furnace.
            - 'recipe' (str): The updated name of the associated recipe.
        oldName (str): The old name of the furnace to be updated.

    Exceptions:
        If an error occurs during the update, an error message is printed, the transaction is rolled back, 
        and the database connection is closed after the operation is complete.
    """
    print(furnace)
    try:
        conn = connect_to_db()
        cur = conn.cursor()
    
        cur.execute("""UPDATE furnaces_table SET furnace_name = ?, recipe_key = ?, start_time = ? WHERE primary_id = ? """, (furnace['furnace_name'],furnace['recipe_key'], furnace['start_time'][0:10],   furnace['primary_id']))

        conn.commit()
    except Exception as e:
        print(f"failed to update furnace: {e}")

        conn.rollback()
        #updated_furnace = {}
    finally:
        conn.close()
    
def update_blocks(recipe, blocks):
    """
    Update the blocks associated with a given recipe in the 'blockname_table' in the SQLite database.

    This function deletes all existing blocks for the given recipe from the 'blockname_table' and then inserts
    the provided list of new blocks for that recipe.

    Args:
        recipe (dict): A dictionary containing the recipe details. Expected key:
            - 'recipe_name' (str): The name of the recipe whose blocks are to be updated.
        blocks (list of dict): A list of dictionaries, each containing the block details. Each dictionary should have the following keys:
            - 'recipe_key' (str): The key representing the associated recipe.
            - 'block' (str): The name of the block.
            - 'sequence' (float): The sequence number for the block.

    Behavior:
        - The function first deletes all existing blocks related to the given recipe.
        - It then inserts the new blocks for the recipe, ensuring foreign key constraints are enforced.
        - The changes are committed to the database.
    """
    updated_furnace = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
      
        cur.execute("DELETE FROM blockname_table WHERE recipe_key = ?", (recipe['recipe_name'],))
        cur.execute("PRAGMA foreign_keys=ON")
        
        for i in range(len(blocks)):
            print(blocks[i])
            cur.execute("INSERT INTO blockname_table (recipe_key, block, sequence) VALUES (?, ?, ?)", (blocks[i]['recipe_key'], blocks[i]['block'], blocks[i]['sequence']))    
        conn.commit()
        print_database()
       
    except Exception as e:
        print(f"failed to update blocks: {e}")

        conn.rollback()
        #updated_furnace = {}
    finally:
        conn.close()

def delete_furnace_recipe(selected):
    """
    Delete a furnace and its associated records from the SQLite database.

    This function deletes the specified furnace from the 'furnace_recipe_table' and 'furnaces_table',
    and also deletes all related entries in the 'calendar_table' that reference the furnace.

    Args:
        selected (str): The name of the furnace to be deleted.

    Behavior:
        - The function deletes the furnace entry from the 'furnace_recipe_table'.
        - It retrieves all primary IDs associated with the furnace from the 'furnaces_table'.
        - The furnace is then deleted from the 'furnaces_table'.
        - If any primary IDs were found, the related entries in the 'calendar_table' are deleted.
        - Changes are committed to the database.

    Exceptions:
        If an error occurs during the deletion, an error message is printed, the transaction is rolled back,
        and the database connection is closed after the operation is complete.
    """
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
     

        cursor.execute("DELETE from furnace_recipe_table WHERE furnace = ?", (selected,))
        cursor.execute("SELECT primary_id FROM furnaces_table WHERE furnace_name = ?", (selected,))
        primary_ids = cursor.fetchall()  # Get all primary_ids as a list of tuples
        print(primary_ids)
        cursor.execute("DELETE from furnaces_table WHERE furnace_name = ?", (selected,))

      
        if primary_ids:
            # Convert the list of tuples to a flat list of primary_ids
            primary_ids = [pid[0] for pid in primary_ids]
            print("primary_ids")
            cursor.executemany("DELETE FROM calendar_table WHERE furnace_id = ?", [(pid,) for pid in primary_ids])
            print("success")
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error while deleting furnace_recipe: {e}")
    finally:
        conn.close()


def delete_recipe(recipe_id):
    """
    Delete a recipe and its associated blocks from the SQLite database.

    This function deletes a specific recipe from the 'recipe_table' and deletes all related entries
    in the 'blockname_table' that reference the recipe.

    Args:
        recipe_id (int): The ID of the recipe to be deleted.

    Behavior:
        - The function retrieves the recipe name using the given recipe ID.
        - It deletes all related blocks from the 'blockname_table' using the fetched recipe name.
        - The recipe is then deleted from the 'recipe_table'.
        - If successful, a success message is stored in the `message` dictionary.
        - If an error occurs, a failure message is stored, and the transaction is rolled back.

    Returns:
        dict: A dictionary containing the status of the operation.

    Exceptions:
        If an error occurs during the deletion, an error message is printed, the transaction is rolled back,
        and the database connection is closed after the operation is complete.
    """
    message = {}
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute("SELECT recipe_name FROM recipe_table WHERE recipe_id = ?", (recipe_id,))
        result = cursor.fetchone()
        if result:
            recipe_key = result[0]
            print(recipe_key)
            # Delete related entries from blockname_table using the fetched recipe_key
            cursor.execute("DELETE FROM blockname_table WHERE recipe_key = ?", (recipe_key,))
            
            # Delete the recipe from recipe_table
            conn.execute("DELETE FROM recipe_table WHERE recipe_id = ?", (recipe_id,))
            
            conn.commit()
            message["status"] = "Recipe and related blocks deleted successfully"
            print(message["status"])

    except Exception as e:
        conn.rollback()
        message["status"] = "Cannot delete recipe"
        print(f"Error while deleting recipe: {e}")
    finally:
        conn.close()

def delete_furnace(primary_id):
    """
    Delete a furnace and its associated calendar entries from the SQLite database.

    This function deletes a specific furnace from the 'furnaces_table' and deletes all related entries
    in the 'calendar_table' that reference the furnace.

    Args:
        primary_id (int): The primary ID of the furnace to be deleted.

    Behavior:
        - The function deletes the furnace from the 'furnaces_table' using the provided primary ID.
        - It then deletes all related entries from the 'calendar_table' that reference the furnace's ID.
        - If successful, a success message is stored in the `message` dictionary.
        - If an error occurs, a failure message is stored, and the transaction is rolled back.

    Returns:
        dict: A dictionary containing the status of the operation.

    Exceptions:
        If an error occurs during the deletion, an error message is printed, the transaction is rolled back,
        and the database connection is closed after the operation is complete.
    """
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from furnaces_table WHERE primary_id = ?", (primary_id,))
        conn.execute("DELETE from calendar_table WHERE furnace_id = ?", (str(primary_id),))

        conn.commit()
        message["status"] = "Furnace deleted successfully"
    except Exception as e:
        conn.rollback()
        message["status"] = "Cannot delete Furnace"
        print(f"Error while deleting furnace{e}")
    finally:
        conn.close()


def print_database():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM recipe_table")
    items = cur.fetchall()
    for item in items:
        print(item)


def main():
    print("main")
    create_furnace_recipe_table()

if __name__ == "__main__":
    main()
