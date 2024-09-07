import React from "react";
import API from "../api";
import { Popover, Box, Button, TextField } from "@mui/material";
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline";
/**
 * PopoverForm Component
 * Renders a button that opens a popover form to add or update a furnace process for an empty block.
 * Displays read-only fields for furnace name, recipe, and start date, and allows the user to submit the form.
 *
 * @param {string} date - The start date for the process.
 * @param {string} recipe - The recipe name.
 * @param {string} furnaceName - The furnace name.
 * @param {Array} apiData - Data from the API related to recipes.
 * @param {Array} furnaceData - Data related to furnaces.
 * @param {Array} blockData - Block data associated with processes.
 * @param {boolean} emptyRow - Flag indicating whether this is an empty row (true for update, false for add).
 * @returns {JSX.Element} The rendered component.
 */
const PopoverForm = ({
  date,
  recipe,
  furnaceName,
  apiData,
  furnaceData,
  blockData,
  emptyRow,
}) => {
  const [anchorEl, setAnchorEl] = React.useState(null);
  const open = Boolean(anchorEl);
  const id = open ? "simple-popover" : undefined;
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
    console.log(date);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };
  // Group block data by recipe_key

  const groupedByRecipeKey = blockData.reduce((acc, item) => {
    const { recipe_key, sequence } = item;
    if (!acc[recipe_key]) {
      acc[recipe_key] = [];
    }
    acc[recipe_key].push(sequence);
    return acc;
  }, {});
  const handleSubmit = () => {
    let newFurnace = {
      furnace_name: furnaceName,
      recipe_key: recipe,
      start_time: date,
    };
    let blocks = groupedByRecipeKey[recipe];
    // const sequenceAsString = blocks.join('')
    // console.log(sequenceAsString)
    let threeBlocks = ["Starting", "Running", "Finishing"];
    let fourBlocks = ["Starting", "Preparing", "Running", "Finishing"];
    let itemList = [];

    if (blocks.length === 3) {
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
    console.log(itemList);
    let postData = [newFurnace, itemList];
    console.log(postData);
    if (emptyRow) {
      const emptyFurnace = furnaceData.find(
        (furnace) => furnace["furnace_name"] === furnaceName
      );
      const idEmpty = emptyFurnace["primary_id"];
      newFurnace = {
        primary_id: idEmpty,
        furnace_name: furnaceName,
        recipe_key: recipe,
        start_time: date,
      };
      postData = [newFurnace, itemList];
      API({
        method: "PUT",
        url: "/api/furnaces/update",
        data: postData,
      })
        .then((response) => {
          window.location.reload();
          //setID(-1);
        })
        .catch((er) => console.log(er));
    } else {
      API({
        method: "POST",
        url: "/api/furnaces/add",
        data: postData,
      })
        .then((response) => {
          //console.log(response);
          window.location.reload();
          //console.log(res)
        })
        .catch((er) => console.log(er));
    }
  };

  return (
    <div>
      <Button
        style={{ textTransform: "none", color: "white" }}
        aria-describedby={id}
        variant="text"
        onClick={handleClick}
      >
        {<AddCircleOutlineIcon> {"Add Process"}</AddCircleOutlineIcon>}
      </Button>
      <Popover id={id} open={open} anchorEl={anchorEl} onClose={handleClose}>
        <Box sx={{ p: 2, width: 300 }}>
          <TextField
            label="Furnace Name"
            value={furnaceName}
            fullWidth
            margin="normal"
            InputProps={{
              readOnly: true,
            }}
          />
          <TextField
            label="Recipe Name"
            value={recipe}
            fullWidth
            margin="normal"
            InputProps={{
              readOnly: true,
            }}
          />
          <TextField
            label="Start Date"
            value={date}
            fullWidth
            margin="normal"
            InputProps={{
              readOnly: true,
            }}
          />
          <Button
            variant="contained"
            color="primary"
            onClick={handleSubmit}
            fullWidth
          >
            Add Process
          </Button>
        </Box>
      </Popover>
    </div>
  );
};

export default PopoverForm;
