import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import Button from "@mui/material/Button";
import AddIcon from "@mui/icons-material/Add";

import {
  TextField,
  Select,
  FormControl,
  InputLabel,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
} from "@mui/material";

import React, { useState } from "react";
import API from "../api";
/**
 * FurnaceTable Component
 * Renders a table displaying furnaces and their associated recipes.
 * Provides functionality to add, edit, and delete furnace entries.
 * @param {Object} props - The component props.
 * @param {Array} props.apiData - List of available recipes.
 * @param {Array} props.furnaceData - List of existing furnace processes.
 * @param {Array} props.blockData - Block data associated with recipes.
 * @param {Array} props.furnaceRecipeData - List of furnace and recipe associations.
 * @returns {JSX.Element} The rendered component.
 */
const FurnaceTable = ({
  apiData,
  furnaceData,
  blockData,
  furnaceRecipeData,
}) => {
  const recipeNames = apiData.map((recipe) => recipe.recipe_name);
  const [anchorEl, setAnchorEl] = React.useState(null);

  const [openModal, setOpenModal] = useState(false);

  const handleOpenModal = () => {
    setOpenModal(true);
  };

  const handleCloseModal = () => {
    setName(null);
    setRecipe("Select");
    setOpenModal(false);
  };

  const open = Boolean(anchorEl);

  const groupedByRecipeKey = blockData.reduce((acc, item) => {
    const { recipe_key, sequence } = item;
    if (!acc[recipe_key]) {
      acc[recipe_key] = [];
    }
    acc[recipe_key].push(sequence);
    return acc;
  }, {});
  // State variables for managing form inputs, modals, and menus

  const [name, setName] = useState(null); // adds a name and recipe
  const [recipe, setRecipe] = useState("Select");

  const [uName, usetName] = useState(""); // updates Name and Recipe
  const [uRecipe, usetRecipe] = useState("");
  const [oldName, setOldName] = useState(); // keeps track of the oldName in case you change the furnace Name
  // changing the furnace name breaks the program however :(

  const [selectedName, setSelectedName] = useState(""); // used to determine what row the edit has been pressed
  const isFormValid = name && recipe !== "Select"; // makes sure that the name is not null and recipe is not the default
  const isUpdateValid = uName && uRecipe;

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };
  const handleSubmit = (event) => {
    event.preventDefault();
    let newFurnace = {
      furnace_name: name,
      recipe_key: recipe,
      start_time: null,
    };
    let blocks = groupedByRecipeKey[recipe];

    let threeBlocks = ["Starting", "Running", "Finishing"];
    let fourBlocks = ["Starting", "Preparing", "Running", "Finishing"];
    let itemList = [];

    if (blocks.length === 3) {
      // based on if it is three blocks or four blocks, the item list follows the sequence
      let count = 0;
      for (const element of threeBlocks) {
        itemList.push({
          furnace_id: -1,
          block: element,
          sequence: blocks[count],
        });
        count += 1;
      }
    } else if (blocks.length === 4) {
      let count = 0;
      for (const element of fourBlocks) {
        itemList.push({
          furnace_id: -1,
          block: element,
          sequence: blocks[count],
        });
        count += 1;
      }
    }
    const postData = [newFurnace, itemList]; // contains the new furnace and the calendar data blocks
    console.log(furnaceRecipeData);
    API({
      method: "POST",
      url: "/api/furnaceRecipe/add",
      data: newFurnace,
    })
      .then((response) => {
        console.log(newFurnace);
        console.log("added");
      })
      .catch((er) => console.log(er));
    API({
      method: "POST",
      url: "/api/furnaces/addRow",
      data: postData,
    })
      .then((response) => {
        window.location.reload();
      })
      .catch((er) => console.log(er));
    handleCloseModal();
  };
  /**
   * handleEdit
   * Takes a furnace and sets the updated data.
   * @param {Object} furnace
   */
  const handleEdit = (furnace) => {
    usetName(furnace.furnace);
    usetRecipe(furnace.recipe);
    setSelectedName(furnace.furnace);
    setOldName(furnace.furnace);
  };
  const handleUpdate = () => {
    // if the update button is pressed
    let new_furnace = {
      furnace: uName,
      recipe: uRecipe,
    };
    const postData = [new_furnace, oldName];
    console.log(postData);

    API({
      method: "PUT",
      url: "/api/furnaceRecipe/update",
      data: postData,
    })
      .then((response) => {
        window.location.reload();
      })
      .catch((er) => console.log(er));
  };
  /**
   * handleDelete
   * handleDelete takes a selected furnace object and uses the furnace name to delete the selected row.
   * @param {Object} selected
   */
  const handleDelete = (selected) => {
    const delete_url = "/api/furnaceRecipes/delete/" + selected["furnace"];
    console.log(delete_url);
    API({
      method: "DELETE",
      url: delete_url,
    })
      .then((response) => {
        window.location.reload();
      })
      .catch((er) => console.log(er));
  };
  /**
   *
   * @param {event} events
   * @param {number} index
   */
  const handleMenu = (events, index) => {
    usetRecipe(recipeNames[index]);
    setAnchorEl(null);
  };
  const handleNameChange = (e) => {
    const newValue = e.target.value;
    usetName(newValue);
  };
  return (
    <div className="container">
      <Button color="primary" startIcon={<AddIcon />} onClick={handleOpenModal}>
        Add New Furnace
      </Button>
      <Dialog open={openModal} onClose={handleCloseModal}>
        <DialogTitle>Add New Furnace</DialogTitle>
        <DialogContent sx={{ width: 400 }}>
          <form onSubmit={handleSubmit}>
            <TextField
              label="Enter Furnace Name"
              variant="outlined"
              onChange={(e) => setName(e.target.value)}
              fullWidth
              margin="normal"
            />
            <FormControl fullWidth margin="normal">
              <InputLabel id="recipe-select-label">Select Recipe</InputLabel>
              <Select
                labelId="recipe-select-label"
                id="recipe-select"
                value={recipe}
                onChange={(e) => setRecipe(e.target.value)}
                label="Select Recipe"
              >
                {recipeNames.map((formRecipes, index) => (
                  <MenuItem key={`${formRecipes}-${index}`} value={formRecipes}>
                    {formRecipes}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <Button
              type="submit"
              variant="contained"
              color="primary"
              disabled={!isFormValid}
              fullWidth
              sx={{ mt: 2 }}
              onClick={handleSubmit}
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
            <th>Furnace Name</th>
            <th>Recipe Name</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {furnaceRecipeData.map((furnace, index) =>
            furnace.furnace === selectedName ? (
              <tr key={`${furnace}-${index}`}>
                <td>
                  <input
                    type="text"
                    value={uName}
                    onChange={handleNameChange}
                  />
                </td>
                <td>
                  <Button
                    variant="contained"
                    id="basic-button"
                    color="success"
                    aria-controls={open ? "basic-menu" : undefined}
                    aria-haspopup="true"
                    aria-expanded={open ? "true" : undefined}
                    onClick={handleClick}
                  >
                    {uRecipe}
                  </Button>
                  <Menu
                    id="basic-menu"
                    anchorEl={anchorEl}
                    open={open}
                    onClose={handleClose}
                    MenuListProps={{
                      "aria-labelledby": "basic-button",
                    }}
                  >
                    {recipeNames.map((recipes, index) => (
                      <MenuItem
                        key={`${recipes}-${index}`}
                        onClick={(event) => handleMenu(event, index)}
                      >
                        {recipes}
                      </MenuItem>
                    ))}
                  </Menu>
                </td>
                <td>
                  <button onClick={handleUpdate} disabled={!isUpdateValid}>
                    Update
                  </button>
                </td>
              </tr>
            ) : (
              <tr key={index}>
                <td>{furnace.furnace}</td>
                <td>{furnace.recipe}</td>
                <td>
                  <button onClick={() => handleEdit(furnace)}> edit </button>
                  <button onClick={() => handleDelete(furnace)}>
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
export default FurnaceTable;
