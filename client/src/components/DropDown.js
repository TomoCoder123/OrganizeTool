import { useState } from "react";
import * as React from "react";
import Divider from "@mui/material/Divider";
import Paper from "@mui/material/Paper";
import MenuList from "@mui/material/MenuList";
import MenuItem from "@mui/material/MenuItem";
import Popover from "@mui/material/Popover";
import FormGroup from "@mui/material/FormGroup";
import Button from "@mui/material/Button";
import Menu from "@mui/material/Menu";
import NumberInputBasic from "./NumInput";
import Modal from "@mui/material/Modal";
import Fade from "@mui/material/Fade";
import Box from "@mui/material/Box";

import ListItemText from "@mui/material/ListItemText";
import ListItemIcon from "@mui/material/ListItemIcon";
import Edit from "@mui/icons-material/Edit";
import PowerOff from "@mui/icons-material/PowerOff";
import Cancel from "@mui/icons-material/Cancel";

import API from "../api";
/**
 * IconMenu Component
 * A menu component that provides various actions (Edit, Abort, Down) for a block in a calendar.
 * It handles the display of popovers and modals for input and confirmation. Only for a currently occupied block.
 *
 * @param {Object} props - The component props.
 * @param {string} name - The name of the block.
 * @param {number} id - The ID of the block.
 * @param {string} state - The current state of the block.
 * @param {Array} calendarData - The data related to calendar blocks.
 * @param {number} curIndex - The current index in the calendar.
 * @param {Array} downData - The list of possible down reasons.
 * @param {boolean} killed - A flag indicating if the block is killed (true/false).
 * @returns {JSX.Element} The rendered IconMenu component.
 */
export default function IconMenu({
  name,
  id,
  state,
  calendarData,
  curIndex,
  downData,
  killed,
}) {
  const [anchorElAdd, setAnchorElAdd] = React.useState(null);
  const [anchorElAbort, setAnchorElAbort] = React.useState(null);
  const [anchorElDown, setAnchorElDown] = React.useState(null);
  const [modalAbortOpen, setModalAbortOpen] = React.useState(false);
  const [modalDownOpen, setModalDownOpen] = React.useState(false);

  const handleAbortOpen = () => setModalAbortOpen(true);
  const handleAbortClose = () => setModalAbortOpen(false);
  const handleDownOpen = (down) => {
    console.log(down);
    setModalDownOpen(true);
    setDownReason(down);
  };
  const handleDownClose = () => {
    setModalDownOpen(false);
    setDownReason(null);
  };
  let validDelete = false;
  let validAdd = false;

  const [uAddRemove, setuAddRemove] = useState(null);
  const [downReason, setDownReason] = useState(null);

  const downReasons = downData.map((down) => down.down_name);

  const handlePopoverOpen = (event, action) => {
    if (action === "add") {
      setAnchorElAdd(event.currentTarget);
    } else if (action === "abort") {
      setAnchorElAbort(event.currentTarget);
    } else if (action === "down") {
      setAnchorElDown(event.currentTarget);
    }
  };
  const handlePopoverClose = (event, action) => {
    if (action === "add") {
      setAnchorElAdd(null);
    } else if (action === "abort") {
      setAnchorElAbort(null);
    } else if (action === "down") {
      setAnchorElDown(null);
    }
  };
  const style = {
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    width: 400,
    bgcolor: "background.paper",
    border: "2px solid #000",
    boxShadow: 24,
    p: 4,
  };
  const handleSubmit = (event, action) => {
    console.log(downReason);
    let updateData = [];
    if (action === "change") {
      updateData = [uAddRemove, state, id, "addremove"];
    } else if (action === "abort") {
      updateData = [curIndex, state, id, "abort"];
    } else {
      updateData = [curIndex, state, id, action];
      console.log(updateData);
    }
    API({
      method: "PUT",
      url: "/api/calendar/update",
      data: updateData,
    })
      .then((response) => {
        window.location.reload();
      })
      .catch((er) => console.log(er));
    handlePopoverClose(event, action);
  };

  const handleTextFieldChange = (event, value) => {
    setuAddRemove(value);
  };
  const blocks = calendarData.filter(
    (block) => block.furnace_id === id.toString()
  );
  let lengths_obj = {};

  const length_list = blocks.map((item, index) => {
    let length;
    if (index < blocks.length - 1) {
      // Length is the difference between the next sequence and the current sequence
      length = blocks[index + 1].sequence - item.sequence;
    } else {
      // For the last item, length is the difference between end_time and sequence
      length = item.end_time - item.sequence;
    }
    lengths_obj[item["block"]] = length;
    return length;
  });
  // validates the add or remove functionality.
  if (
    uAddRemove < 0 &&
    lengths_obj[state] > parseInt(-uAddRemove) &&
    length_list
  ) {
    validDelete = true;
  }
  if (uAddRemove > 0) {
    validAdd = true;
  }
  const validContinue = !killed;
  let validSubmit =
    uAddRemove !== null &&
    uAddRemove !== undefined &&
    uAddRemove !== 0 &&
    uAddRemove !== "" &&
    !isNaN(uAddRemove) &&
    (validDelete || validAdd) &&
    !killed;

  return (
    <div>
      <div>
        <Paper sx={{ width: 200, maxWidth: "100%" }}>
          <MenuList>
            <MenuItem
              aria-owns={
                Boolean(anchorElAdd) ? "mouse-over-popover" : undefined
              }
              aria-haspopup="true"
              onMouseEnter={(event) => handlePopoverOpen(event, "add")}
              onMouseLeave={(event) => handlePopoverClose(event, "add")}
            >
              <ListItemIcon>
                <Edit fontSize="small" />
              </ListItemIcon>
              <ListItemText>Edit Block(s)</ListItemText>
              <Popover
                id="mouse-over-popover"
                sx={{
                  pointerEvents: "none",
                }}
                open={Boolean(anchorElAdd)}
                anchorEl={anchorElAdd}
                anchorOrigin={{
                  vertical: "top",
                  horizontal: "right",
                }}
                transformOrigin={{
                  vertical: "top",
                  horizontal: "left",
                }}
                onClose={(event) => handlePopoverClose(event, "add")}
                disableRestoreFocus
              >
                <div>
                  <FormGroup
                    sx={{
                      padding: 2,
                      borderRadius: 2,
                      border: "1px solid",
                      borderColor: "primary.main",
                      pointerEvents: "auto",
                    }}
                  >
                    <NumberInputBasic
                      aria-label="Demo number input"
                      placeholder="Type a number…"
                      value={uAddRemove}
                      onChange={handleTextFieldChange}
                    />
                    <Button
                      variant="outlined"
                      disabled={!validSubmit}
                      value={uAddRemove}
                      onClick={(event) => handleSubmit(event, "change")}
                    >
                      Submit
                    </Button>
                  </FormGroup>
                </div>
              </Popover>
            </MenuItem>
            <MenuItem
              aria-owns={
                Boolean(anchorElAbort) ? "mouse-over-popover3" : undefined
              }
              aria-haspopup="true"
              onMouseEnter={(event) => handlePopoverOpen(event, "abort")}
              onMouseLeave={(event) => handlePopoverClose(event, "abort")}
            >
              <ListItemIcon>
                <Cancel fontSize="small" />
              </ListItemIcon>
              <ListItemText>Abort</ListItemText>
              <Popover
                id="mouse-over-popover3"
                sx={{
                  pointerEvents: "none",
                }}
                open={Boolean(anchorElAbort)}
                anchorEl={anchorElAbort}
                anchorOrigin={{
                  vertical: "top",
                  horizontal: "right",
                }}
                transformOrigin={{
                  vertical: "top",
                  horizontal: "left",
                }}
                onClose={(event) => handlePopoverClose(event, "abort")}
                disableRestoreFocus
              >
                <form>
                  <FormGroup
                    sx={{
                      padding: 2,
                      borderRadius: 2,
                      border: "1px solid",
                      borderColor: "primary.main",
                      pointerEvents: "auto",
                    }}
                  >
                    <Button
                      variant="outlined"
                      disabled={!validContinue}
                      onClick={handleAbortOpen}
                    >
                      Continue
                    </Button>
                  </FormGroup>
                </form>
              </Popover>
            </MenuItem>
            <Divider />
            <MenuItem
              aria-owns={
                Boolean(anchorElDown) ? "mouse-over-popover4" : undefined
              }
              aria-haspopup="true"
              onMouseEnter={(event) => handlePopoverOpen(event, "down")}
              onMouseLeave={(event) => handlePopoverClose(event, "down")}
            >
              <ListItemIcon>
                <PowerOff fontSize="small" />
              </ListItemIcon>
              <ListItemText>Down</ListItemText>

              <Menu
                id="mouse-over-popover4"
                anchorEl={anchorElDown}
                open={Boolean(anchorElDown)}
                onClose={(event) => handlePopoverClose(event, "down")}
              >
                {downReasons.map((down, index) => (
                  <MenuItem
                    key={`${down}-${index}`}
                    onClick={() => handleDownOpen(down)}
                    disabled={!validContinue}
                  >
                    {down}
                  </MenuItem>
                ))}
              </Menu>
            </MenuItem>
          </MenuList>
        </Paper>
      </div>
      <div>
        <Modal
          open={modalAbortOpen}
          onClose={handleAbortClose}
          aria-labelledby="modal-modal-title"
          aria-describedby="modal-modal-description"
        >
          <Fade in={modalAbortOpen}>
            <div>
              <Box sx={style}>
                <h2 id="modal-modal-title">Warning</h2>
                <p id="modal-modal-description">
                  Clicking submit will abort the process!{" "}
                </p>
                <Button onClick={(event) => handleSubmit(event, "abort")}>
                  Submit
                </Button>
              </Box>
            </div>
          </Fade>
        </Modal>
        <Modal
          open={modalDownOpen}
          onClose={handleDownClose}
          aria-labelledby="modal-down-title"
          aria-describedby="modal-down-description"
        >
          <Fade in={modalDownOpen}>
            <div>
              <Box sx={style}>
                <h2 id="modal-down-title">Warning</h2>
                <p id="modal-down-description">
                  Clicking submit will end the selected run!{" "}
                </p>
                <Button onClick={(event) => handleSubmit(event, downReason)}>
                  Submit
                </Button>
              </Box>
            </div>
          </Fade>
        </Modal>
      </div>
    </div>
  );
}
