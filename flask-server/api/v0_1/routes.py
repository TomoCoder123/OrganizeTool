import sys
import os
from flask import current_app, request, jsonify, make_response, Blueprint
import json
current_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(current_dir,'..','..', 'sqlite'))
import database
from datetime import datetime


VERSION = "0.1"

blueprint_ver_str = VERSION.replace(".", "_")  # replace dot with underscore
url_ver_str = VERSION.replace(".", "-")   # replace dot with dash
api = Blueprint(f"api_v{blueprint_ver_str}", __name__)  

# ---- API Health ----


@api.route("/health-check", methods=["GET"])
def health_check():
    """
    Perform a health check for the API.

    This endpoint checks the health and connectivity of the API and returns a JSON response 
    indicating that the connection is successfully established.

    Returns:
        tuple: A tuple containing:
            - A JSON response with the following keys:
                - 'code' (int): The HTTP status code (200).
                - 'success' (bool): Indicates whether the health check was successful (True).
                - 'message' (str): A message indicating the connection status.
            - An HTTP status code (int): 200 if the connection is established.
    """
    res = {"code": 200, "success": True, "message": "Connection Established"}
    return jsonify(res), res["code"]


@api.route("/process-recipes", methods=["GET"])
def get_recipes():
    """
    Retrieve and return recipe data from a JSON file.

    This endpoint reads the 'recipes.json' file from the 'config_files' directory and 
    returns the recipe data in JSON format.

    The JSON file is located two directories up from the current file's directory 
    and inside the 'config_files' folder.

    Returns:
        Response: A Flask `jsonify` response containing the recipe data as JSON.
    """
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'config_files', 'recipes.json')
    with open(json_path, 'r') as file:
        data = json.load(file)
    return jsonify(data)


@api.route('/api/recipes', methods=['GET'])
def api_get_recipes():
    """
    Retrieve all recipes from the database.

    This endpoint retrieves all recipe data from the database and returns it in JSON format.

    Returns:
        Response: A Flask `jsonify` response containing a list of recipes.
    """
    return jsonify(database.read_recipes())
@api.route('/api/furnaceRecipes', methods=['GET'])
def api_get_furnace_recipes():
    """
    Retrieve all furnace recipes from the database.

    This endpoint retrieves all furnace recipe data from the lookup table furnace_recipe and returns it in JSON format.

    Returns:
        Response: A Flask `jsonify` response containing a list of furnace recipes.
    """
    return jsonify(database.read_furnace_recipes())

@api.route('/api/furnaces', methods=['GET'])
def api_get_furnaces():
    """
    Retrieve all furnaces from the database.

    This endpoint retrieves all furnace data from the database and returns it in JSON format.

    Returns:
        Response: A Flask `jsonify` response containing a list of furnaces.
    """
    return jsonify(database.read_furnaces())

@api.route('/api/blocks', methods=['GET'])
def api_get_blocks():
    """
    Retrieve all blocks from the database.

    This endpoint retrieves all block data from the database and returns it in JSON format.

    Returns:
        Response: A Flask `jsonify` response containing a list of blocks.
    """
    return jsonify(database.read_blocks())

@api.route('/api/colors', methods=['GET'])
def api_get_colors():
    """
    Retrieve all colors from the database.

    This endpoint retrieves all color data from the database and returns it in JSON format.

    Returns:
        Response: A Flask `jsonify` response containing a list of colors.
    """
    return jsonify(database.read_colors())

@api.route('/api/calendar', methods=['GET'])
def api_get_calendar():
    """
    Retrieve all calendar entries from the database.

    This endpoint retrieves all calendar data from the database and returns it in JSON format.

    Returns:
        Response: A Flask `jsonify` response containing a list of calendar entries.
    """
    return jsonify(database.read_calendar())
@api.route('/api/downreasons', methods=['GET'])
def api_get_down():
    """
    Retrieve all down reasons from the database.

    This endpoint retrieves all down reason data from the database and returns it in JSON format.

    Returns:
        Response: A Flask `jsonify` response containing a list of down reasons.
    """
    return jsonify(database.read_down())


@api.route('/api/recipes/<recipe_id>', methods=['GET'])
def api_get_recipe(recipe_id):
    """
    Retrieve a specific recipe by its ID from the database.

    This endpoint retrieves the recipe data for the given recipe ID from the database 
    and returns it in JSON format.

    Args:
        recipe_id (int): The ID of the recipe to retrieve.

    Returns:
        Response: A Flask `jsonify` response containing the recipe data.
    """
    return jsonify(database.read_recipe_by_id(recipe_id))


@api.route('/api/furnaces/<primary_id>', methods=['GET'])
def api_get_furnace(primary_id):
    """
    Retrieve a specific furnace by its ID from the database.

    This endpoint retrieves the furnace data for the given primary ID from the database 
    and returns it in JSON format.

    Args:
        primary_id (int): The primary ID of the furnace to retrieve.

    Returns:
        Response: A Flask `jsonify` response containing the furnace data.
    """
    return jsonify(database.read_furnace_by_id(primary_id))


@api.route('/api/recipes/add',  methods=['POST'])
def api_add_recipe():
    """
    Add a new recipe to the database.

    This endpoint allows the client to add a new recipe by sending a JSON payload 
    containing the recipe details. The 'time' field must be a float. The recipe is added 
    to the database if valid.

    Expected JSON payload:
        - 'recipe_name' (str): The name of the recipe.
        - 'time' (float): The time associated with the recipe.

    Returns:
        Response:
            - If successful: A Flask `jsonify` response containing the newly created recipe.
            - If 'time' is not a valid float: A 400 Bad Request response with an error message.
            - If any other error occurs: A 500 Internal Server Error response with an error message.
    """
    recipe = request.get_json()
    try:
        recipe['time'] = float(recipe['time'])
        return jsonify(database.create_recipe(recipe))
    except TypeError:
        return (jsonify({"error": "Invalid value for time. Must be a float."}), 400)  # HTTP 400 Bad Request
    except Exception as e:
        print(f"{e}")
        return (jsonify({"error": "An error occurred while adding the recipe."}), 500)
@api.route('/api/furnaceRecipe/add',  methods=['POST'])
def api_add_furnace_recipe():
    """
    Add a new furnace recipe to the database.

    This endpoint allows the client to add a new furnace recipe by sending a JSON payload 
    containing the furnace recipe details. The furnace recipe is added to the database if valid.

    Expected JSON payload:
        - 'furnace' (str): The name of the furnace.
        - 'recipe' (str): The name of the associated recipe.

    Returns:
        Response:
            - If successful: A Flask `jsonify` response containing the newly created furnace recipe.
            - If any error occurs: A 500 Internal Server Error response with an error message.
    """
    furnace_recipe = request.get_json()
    try:
        return jsonify(database.create_furnace_recipe(furnace_recipe))
    except Exception as e:
        print(f"{e}")
        return (jsonify({"error": "An error occurred while adding the furnace recipe."}), 500)
    
    

@api.route('/api/recipes/add/<blocks>',  methods=['POST'])
def api_add_recipe_blocks(blocks):
    """
    Add a new recipe along with its blocks to the database.

    This endpoint allows the client to add a new recipe by sending a JSON payload containing 
    the recipe details. If the recipe is successfully added, the associated blocks are also 
    created in the 'blockname_table' based on the length of the 'blocks' argument.

    Expected JSON payload:
        - 'recipe_name' (str): The name of the recipe.
        - 'time' (float): The time associated with the recipe.

    Args:
        blocks (list): A list of sequence numbers representing the blocks to be associated with the recipe.

    Behavior:
        - If the length of 'blocks' is 3, it creates 'Starting', 'Running', and 'Finishing' blocks.
        - If the length of 'blocks' is 4, it creates 'Starting', 'Preparing', 'Running', and 'Finishing' blocks.

    Returns:
        Response:
            - If successful: A Flask `jsonify` response containing the newly created recipe and blocks.
            - If 'time' is not a valid float: A 400 Bad Request response with an error message.
            - If any other error occurs: A 500 Internal Server Error response with an error message.
    """
    recipe = request.get_json()
    try:
        print(len(blocks))
        new_recipe = jsonify(database.create_recipe(recipe))
        if (len(blocks) == 3):
            block1 = {'recipe_key':recipe['recipe_name'], 'block': 'Starting', 'sequence': blocks[0] }
            block2 = {'recipe_key':recipe['recipe_name'], 'block': 'Running', 'sequence': blocks[1] }
            block3 = {'recipe_key':recipe['recipe_name'], 'block': 'Finishing', 'sequence': blocks[2] }
            block_list = [block1, block2, block3]
            print(block_list)
            database.create_block(block_list)
     
        elif (len(blocks) == 4):
            block1 = {'recipe_key':recipe['recipe_name'], 'block': 'Starting', 'sequence': blocks[0] }
            block2 = {'recipe_key':recipe['recipe_name'], 'block': 'Preparing', 'sequence': blocks[1] }
            block3 = {'recipe_key':recipe['recipe_name'], 'block': 'Running', 'sequence': blocks[2] }
            block4 = {'recipe_key':recipe['recipe_name'], 'block': 'Finishing', 'sequence': blocks[3] }
            block_list = [block1, block2, block3, block4]

            database.create_block(block_list)
            

        recipe['time'] = float(recipe['time'])
        print("printing blocks from add_recipe_blocks")
        # database.print_blocks()
        return new_recipe
    except TypeError:
        return (jsonify({"error": "Invalid value for time. Must be a float."}), 400)  # HTTP 400 Bad Request
    except Exception as e:
        print(f"{e}")
        return (jsonify({"error": "An error occurred while adding the recipe."}), 500)
    


@api.route('/api/furnaces/addRow',  methods=['POST'])
def api_add_furnaceRow():
    """
    Add a new furnace entry along with calendar entries to the database.

    This endpoint allows the client to add a new furnace entry and its corresponding calendar entries 
    by sending a JSON payload. The JSON payload is expected to contain two parts:
        1. Furnace details as the first item.
        2. A list of calendar entries as the second item.

    Expected JSON payload:
        - Furnace details (dict): A dictionary containing the details of the furnace, such as:
            - 'furnace_name' (str): The name of the furnace.
            - 'recipe_key' (str): The key representing the associated recipe.
            - 'start_time' (str): The start time associated with the furnace.
        - Calendar entries (list): A list of dictionaries, each representing a calendar entry.

    Returns:
        Response:
            - A Flask `jsonify` response containing the result of the furnace creation operation.
            - A 201 Created status code upon successful creation.
    """
    furnace = request.get_json()[0]
    print(furnace)
    calendar_list = request.get_json()[1]

    # Call the database function to create the furnace entry
    result = database.create_furnace(furnace)
    # new_calendar = database.create_calendar(calendar_list, furnace['start_time'], furnace['furnace_name'])
    return jsonify(result), 201  # HTTP 201 Created

@api.route('/api/furnaces/add',  methods=['POST']) #not being used right now
def api_add_furnace():
    furnace = request.get_json()[0]
    print(furnace)
    calendar_list = request.get_json()[1]
    date_formats = ["%Y-%m-%d"]
    parsed = False

    for date_format in date_formats:
        try:
            # Try to parse the date string using the current format
            date_object = datetime.strptime(furnace['start_time'][:10], date_format)
            # If successful, format the date back to a string in the same format and break the loop
            furnace['start_time'] = date_object.strftime(date_format)
            parsed = True
            break
        except Exception as e:
            print(f"{e}")

            continue

    if not parsed:
        print("Bad Request")
        return jsonify({"error": "Invalid value for start_time. Must be in 'MM-DD-YYYY' or 'MM/DD/YYYY' format."}), 400  # HTTP 400 Bad Request

    # Call the database function to create the furnace entry
    result = database.create_furnace(furnace)
    print(calendar_list)
    print(furnace['start_time'])
    print(furnace['furnace_name'])
    new_calendar = database.create_calendar(calendar_list, furnace['start_time'], furnace['furnace_name'])
    return jsonify(result), 201  # HTTP 201 Created


@api.route('/api/recipes/update',  methods=['PUT'])
def api_update_recipe():
    """
    Update an existing recipe in the database.

    This endpoint allows the client to update an existing recipe by sending a JSON payload 
    containing the updated recipe details. The 'time' field must be a float. The recipe 
    is updated in the database if valid.

    Expected JSON payload:
        - 'recipe_id' (int): The ID of the recipe to update.
        - 'recipe_name' (str): The updated name of the recipe.
        - 'time' (float): The updated time associated with the recipe.

    Returns:
        Response:
            - If successful: A Flask `jsonify` response containing the updated recipe.
            - If 'time' is not a valid float: A message is printed indicating the error.
    """
    recipe = request.get_json()
    try:
        recipe['time'] = float(recipe['time'])
        return jsonify(database.update_recipe(recipe))
    except:
        print("Time has to be a float ")

@api.route('/api/calendar/update',  methods=['PUT'])
def api_update_calendar():
    """
    Update an existing calendar entry in the database.

    This endpoint allows the client to update a calendar entry by sending a JSON payload 
    containing the update details. The behavior of the update depends on the action specified 
    in the payload, which can be "abort", "Down", or "addremove".

    Expected JSON payload:
        - The first item (int): The number representing the change in sequence or time.
        - The second item (str): The state of the block to be updated.
        - The third item (int): The ID of the furnace for which the calendar entry is to be updated.
        - The fourth item (str): The action to be performed. This can be:
            - "abort": To update the calendar entry with an abort action.
            - "Down": To add a down reason to the calendar.
            - "addremove": To add or remove time from the calendar entry.

    Returns:
        Response:
            - If successful: A Flask `jsonify` response containing the updated calendar data.
            - If an error occurs: An error message is printed.
    """
    data = request.get_json()
    print(data)
  
    number = data[0]
    state = data[1]
    id = data[2]
        
    try:
        if(data[3] == "abort"):
            return jsonify(database.update_calendar(number, state, id, "abort"))
        elif("Down" in data[3]):
            print("downnnnnn")
            return jsonify(database.update_calendar(number, state, id, data[3]))

            
        else:
            return jsonify(database.update_calendar(number, state, id, "addremove"))
    except Exception as e:
        print(f"Failed to update calendar {e}")

@api.route('/api/recipes/update/<blocks>',  methods=['PUT'])
def api_update_recipes(blocks):
    """
    Update an existing recipe and its associated blocks in the database.

    This endpoint allows the client to update a recipe and its associated blocks by sending 
    a JSON payload with the updated recipe details. The blocks are updated based on the 
    length of the 'blocks' argument.

    Expected JSON payload:
        - 'recipe_id' (int): The ID of the recipe to update.
        - 'recipe_name' (str): The updated name of the recipe.
        - 'time' (float): The updated time associated with the recipe.

    Args:
        blocks (list): A list of sequence numbers representing the blocks to be associated with the recipe.

    Behavior:
        - If the length of 'blocks' is 3, it updates 'Starting', 'Running', and 'Finishing' blocks.
        - If the length of 'blocks' is 4, it updates 'Starting', 'Preparing', 'Running', and 'Finishing' blocks.

    Returns:
        Response: A Flask `jsonify` response containing the updated recipe data, or an error message if an exception occurs.
    """
    recipe = request.get_json()
    try:
        if (len(blocks) == 3):
            block1 = {'recipe_key':recipe['recipe_name'], 'block': 'Starting', 'sequence': blocks[0] }
            block2 = {'recipe_key':recipe['recipe_name'], 'block': 'Running', 'sequence': blocks[1] }
            block3 = {'recipe_key':recipe['recipe_name'], 'block': 'Finishing', 'sequence': blocks[2] }
            block_list = [block1, block2, block3]
            print(block_list)
     
        elif (len(blocks) == 4):
            block1 = {'recipe_key':recipe['recipe_name'], 'block': 'Starting', 'sequence': blocks[0] }
            block2 = {'recipe_key':recipe['recipe_name'], 'block': 'Preparing', 'sequence': blocks[1] }
            block3 = {'recipe_key':recipe['recipe_name'], 'block': 'Running', 'sequence': blocks[2] }
            block4 = {'recipe_key':recipe['recipe_name'], 'block': 'Finishing', 'sequence': blocks[3] }
            block_list = [block1, block2, block3, block4]
        print("made it to second part")
        ret_val = database.update_recipe(recipe)
        database.update_blocks(recipe, block_list)
        return jsonify(ret_val)
    except Exception as e:
        print(f"error while updating recipe: {e} ")


# /api/furnaceRecipes/delete/
@api.route('/api/furnaceRecipes/delete/<selected>',  methods=['DELETE'])
def api_delete_furnace_recipe(selected):
    """
    Delete a furnace recipe from the database.

    This endpoint deletes a furnace recipe from the 'furnace_recipe_table' based on the 
    provided furnace name.

    Args:
        selected (str): The name of the furnace to be deleted from the database.

    Returns:
        Response: A Flask `jsonify` response indicating the result of the delete operation.
    """

    return jsonify(database.delete_furnace_recipe(selected))

@api.route('/api/furnaceRecipe/update',  methods=['PUT'])
def api_update_furnace_recipe():
    """
    Update an existing furnace recipe in the database.

    This endpoint updates an existing furnace recipe by sending a JSON payload containing 
    the updated furnace recipe details and the old furnace name.

    Expected JSON payload:
        - The first item (dict): A dictionary containing the updated furnace recipe details, including:
            - 'furnace' (str): The updated name of the furnace.
            - 'recipe' (str): The updated name of the associated recipe.
        - The second item (str): The old name of the furnace that needs to be updated.

    Returns:
        Response: A Flask `jsonify` response containing the updated furnace recipe data.
    """
    print(request.get_json())
    furnaceRecipe = request.get_json()[0]
    #print(furnace)
    oldName = request.get_json()[1]


    return jsonify(database.update_furnace_recipe(furnaceRecipe, oldName))

@api.route('/api/furnaces/update',  methods=['PUT'])
def api_update_furnace():
    """
    Update an existing furnace entry in the database and create associated calendar entries.

    This endpoint updates an existing furnace by sending a JSON payload containing the updated 
    furnace details and a list of calendar entries. The furnace is updated in the database, and 
    the new calendar entries are created.

    Expected JSON payload:
        - The first item (dict): A dictionary containing the updated furnace details, including:
            - 'furnace_name' (str): The updated name of the furnace.
            - 'recipe_key' (str): The key representing the associated recipe.
            - 'start_time' (str): The start time associated with the furnace.
        - The second item (list): A list of dictionaries, each representing a calendar entry.

    Returns:
        Response: A Flask `jsonify` response containing the updated furnace data.
    """
    furnace = request.get_json()[0]
    calendar_list = request.get_json()[1]

    new_calendar = database.create_empty_calendar(calendar_list, furnace)

    return jsonify(database.update_furnace(furnace))
# cur.execute("""UPDATE furnace_recipe_table SET furnace = ?, recipe_key = ? WHERE primary = ? """, (furnace['furnace_name'],furnace['recipe_key'], furnace['start_time'][0:10],   furnace['primary_id']))

@api.route('/api/recipes/delete/<recipe_id>',  methods=['DELETE'])
def api_delete_recipe(recipe_id):
    """
    Delete a recipe and its associated blocks from the database.

    This endpoint deletes a recipe from the 'recipe_table' based on the provided recipe ID.
    It also deletes all related blocks from the 'blockname_table'.

    Args:
        recipe_id (int): The ID of the recipe to be deleted from the database.

    Returns:
        Response: A Flask `jsonify` response indicating the result of the delete operation.
    """
    return jsonify(database.delete_recipe(recipe_id))

@api.route('/api/furnaces/delete/<furnace_id>',  methods=['DELETE'])
def api_delete_furnace(furnace_id):
    """
    Delete a furnace and its associated calendar entries from the database.

    This endpoint deletes a furnace from the 'furnaces_table' based on the provided furnace ID.
    It also deletes all related entries from the 'calendar_table'.

    Args:
        furnace_id (int): The ID of the furnace to be deleted from the database.

    Returns:
        Response: A Flask `jsonify` response indicating the result of the delete operation.
    """
    return jsonify(database.delete_furnace(furnace_id))

