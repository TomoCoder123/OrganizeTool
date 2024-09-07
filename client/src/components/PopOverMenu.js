import * as React from "react";
import Popover from "@mui/material/Popover";
import Button from "@mui/material/Button";
import IconMenu from "./DropDown";
// import {AddContext} from '../Contexts/AddContext'
// import  { useContext} from 'react'

export default function BasicPopover({
  name,
  idnum,
  state,
  calendarData,
  curIndex,
  downData,
  killed,
}) {
  const [anchorEl, setAnchorEl] = React.useState(null);
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const open = Boolean(anchorEl);
  const id = open ? "simple-popover" : undefined;

  return (
    <div>
      <Button
        style={{
          textTransform: "none",
          color: "black",
          fontSize: name === "Down-Maintenance" ? "10px" : "13px",
        }}
        aria-describedby={id}
        variant="text"
        onClick={handleClick}
      >
        {name}{" "}
      </Button>
      <Popover
        id={id}
        open={open}
        anchorEl={anchorEl}
        onClose={handleClose}
        anchorOrigin={{
          vertical: "bottom",
          horizontal: "left",
        }}
      >
        <IconMenu
          name={name}
          id={idnum}
          state={state}
          calendarData={calendarData}
          curIndex={curIndex}
          downData={downData}
          killed={killed}
        ></IconMenu>
      </Popover>
    </div>
  );
}
