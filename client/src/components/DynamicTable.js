import React, { useState } from "react";
import API from "../api";
import {
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
/**
 * DynamicTable Component
 * Renders a table of recipes, provides functionalities to add, edit, and delete recipes,
 * and displays a modal for adding new recipes.
 * @param {Object} props - The component props.
 * @param {Array} props.jsonData - List of recipes to be displayed.
 * @param {Array} props.recipeList - List of existing recipe names to prevent deletion if in use.
 * @param {Array} props.blockData - Block data associated with recipes.
 * @param {Array} props.colorData - Color data (not currently used).
 * @returns {JSX.Element} The rendered component.
 */
const DynamicTable = ({ jsonData, recipeList, blockData, colorData }) => {
  const [openModal, setOpenModal] = useState(false);

  const handleOpenModal = () => {
    setOpenModal(true);
  };
  const handleCloseModal = () => {
    setBlock("");
    setName("");
    setTime("");
    setOpenModal(false);
  };
  const [name, setName] = useState(""); // adding name, block and time through the form
  const [block, setBlock] = useState("");

  const [time, setTime] = useState("");

  const [uName, usetName] = useState(""); //updating name, time, and block through the edit
  const [uTime, usetTime] = useState("");
  const [uBlock, usetBlock] = useState("");

  const [id, setID] = useState(""); // used to identify the row
  const groupedByRecipeKey = blockData.reduce((acc, item) => {
    // creates an object of the blocks
    // grouped by unique recipe keys
    const { recipe_key, sequence } = item;
    if (!acc[recipe_key]) {
      acc[recipe_key] = [];
    }
    acc[recipe_key].push(sequence);
    return acc;
  }, {});

  // Convert the object into a list format, and concatenate the sequences as strings ie 0135
  const sequencesAsString = {};
  for (const [key, value] of Object.entries(groupedByRecipeKey)) {
    sequencesAsString[key] = value.join("");
  }
  // Handle form submission to add a new recipe

  const handleSubmit = (event) => {
    event.preventDefault();
    let new_recipe = { recipe_name: name, time: time };
    let url_block = "/api/recipes/add/";
    url_block += block;
    API({
      method: "POST",
      url: url_block,
      data: new_recipe,
    })
      .then((response) => {
        window.location.reload();
      })
      .catch((er) => console.log(er));
    handleCloseModal();
  };
  const handleEdit = (recipe) => {
    setID(recipe.recipe_id);
    usetName(recipe.recipe_name);
    usetTime(recipe.time);
    usetBlock(sequencesAsString[recipe.recipe_name]);
  };
  const handleUpdate = () => {
    let new_recipe = { recipe_id: id, recipe_name: uName, time: uTime };
    let url_update = "/api/recipes/update/";
    url_update += uBlock;
    API({
      method: "PUT",
      url: url_update,
      data: new_recipe,
    })
      .then((response) => {
        const res = response.data;
        console.log(res);

        window.location.reload();
        //setID(-1);
        console.log(res);
      })
      .catch((er) => console.log(er));
  };
  const handleDelete = (id) => {
    const delete_url = "/api/recipes/delete/" + id;
    API({
      method: "DELETE",
      url: delete_url,
    }).then((response) => {
      window.location.reload();
    });
  };
  /**
   * checkValid
   * Checks if there are non-null inputs for each name time and block and validates input
   * @param {string} name
   * @param {Date Time} time
   * @param {string} block
   * @returns
   */
  const checkValid = (name, time, block) => {
    if (!name || !time || !block) {
      return false;
    }

    // Check if block has only 3 or 4 characters
    if (block.length < 3 || block.length > 4) {
      return false;
    }

    // Check if each character in block is an integer in increasing order
    // and ensure the last integer is less than time
    if (block[0] !== "0") {
      return false;
    }
    for (let i = 0; i < block.length; i++) {
      // Checks if each block is less than the next, each
      // block is not a space character or non-digit
      const currentChar = block[i];
      const nextChar = block[i + 1];

      if (isNaN(currentChar)) {
        return false;
      }

      const currentInt = parseInt(currentChar, 10);
      if (i < block.length - 1) {
        const nextInt = parseInt(nextChar, 10);

        if (currentInt >= nextInt) {
          return false;
        }
      } else {
        if (currentInt >= time) {
          return false;
        }
      }
    }

    return true;
  };
  let isValidAdd = checkValid(name, time, block);
  let isValidUpdate = checkValid(uName, uTime, uBlock);

  return (
    <div className="container">
      <Button color="primary" startIcon={<AddIcon />} onClick={handleOpenModal}>
        Add New Recipe
      </Button>
      <Dialog open={openModal} onClose={handleCloseModal}>
        <DialogTitle>Add New Recipe</DialogTitle>
        <DialogContent sx={{ width: 400 }}>
          <form onSubmit={handleSubmit}>
            <TextField
              label="Enter Recipe Name"
              variant="outlined"
              onChange={(e) => setName(e.target.value)}
              fullWidth
              margin="normal"
            />
            <TextField
              label="Enter Time"
              variant="outlined"
              onChange={(e) => setTime(e.target.value)}
              fullWidth
              margin="normal"
            />
            <TextField
              label="Enter Sequence"
              variant="outlined"
              onChange={(e) => setBlock(e.target.value)}
              fullWidth
              margin="normal"
            />
            <Button
              type="submit"
              variant="contained"
              color="primary"
              disabled={!isValidAdd}
              fullWidth
              sx={{ mt: 2 }}
            >
              Add
            </Button>
          </form>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseModal} color="primary">
            Cancel
          </Button>
        </DialogActions>
      </Dialog>
      <table>
        <thead>
          <tr>
            <th>Recipe Name</th>
            <th>Time (Days)</th>
            <th>Blocks</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody style={{}}>
          {jsonData.map((recipe, index) =>
            recipe.recipe_id === id ? (
              <tr key={`${recipe}-${index}`}>
                <td>
                  <input
                    type="text"
                    value={uName}
                    onChange={(e) => usetName(e.target.value)}
                  />
                </td>
                <td>
                  <input
                    type="text"
                    value={uTime}
                    onChange={(e) => usetTime(e.target.value)}
                  />
                </td>
                <td>
                  <input
                    type="text"
                    value={uBlock}
                    onChange={(e) => usetBlock(e.target.value)}
                  />
                </td>

                <td>
                  <button onClick={handleUpdate} disabled={!isValidUpdate}>
                    Update
                  </button>
                </td>
              </tr>
            ) : (
              <tr key={index}>
                <td>{recipe.recipe_name}</td>
                <td>{recipe.time}</td>
                <td>{sequencesAsString[recipe.recipe_name]}</td>
                <td>
                  <button onClick={() => handleEdit(recipe)}> edit </button>
                  <button
                    disabled={recipeList.includes(recipe.recipe_name)}
                    onClick={() => handleDelete(recipe.recipe_id)}
                  >
                    {" "}
                    delete{" "}
                  </button>
                </td>
              </tr>
            )
          )}
        </tbody>
      </table>
    </div>
  );
};

export default DynamicTable;
