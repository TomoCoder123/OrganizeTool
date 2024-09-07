import React, { useEffect, useRef } from "react";
import BasicPopover from "./PopOverMenu";
import PopoverForm from "./EmptyPopover";

/**
 * Helper function to determine if a year is a leap year.
 * @param {number} year - The year to check.
 * @returns {number} - The number of days in the year (365 or 366).
 */
function daysInYear(year) {
  return (year % 4 === 0 && year % 100 > 0) || year % 400 === 0 ? 366 : 365;
}

/**
 * Helper function to add a specified number of days to a date.
 * @param {Date} date - The original date.
 * @param {number} days - The number of days to add.
 * @returns {Date} - The new date after adding the specified number of days.
 */
function addDays(date, days) {
  const result = new Date(date);
  result.setDate(result.getDate() + days);
  return result;
}
/**
 * Generates a list of dates between two given dates.
 * @param {Date} strDate - The start date.
 * @param {Date} stpDate - The stop date.
 * @returns {Array<Date>} - An array of dates from the start to the stop date.
 */
function getDate(strDate, stpDate) {
  let dArray = [];
  let cDate = strDate;
  while (cDate <= stpDate) {
    // Adding the date to array
    dArray.push(new Date(cDate));

    // Increment the date by 1 day
    cDate = addDays(cDate, 1);
  }
  return dArray;
}
/**
 * Helper function to determine the number of days in a month.
 * @param {number} month - The month (0-indexed).
 * @param {number} year - The year.
 * @returns {number} - The number of days in the month.
 */
const daysInMonth = (month, year) => {
  return new Date(year, month + 1, 0).getDate(); // month + 1, day 0 gives the last day of the month
};

/**
 * Generates a dictionary containing start times and downtime information for each furnace, used because
 * the map iterates through each furnace name.
 * @param {Array} monthList - The list of months.
 * @param {Array} furList - The list of furnace process data.
 * @param {Array} calendarData - The calendar data containing block events.
 * @param {number} length_recipe - The length of the recipe.
 * @param {string} furnaceName - The name of the furnace.
 * @param {Array} furnaceRecipeData - The data for furnace recipes.
 * @returns {Object} - A dictionary containing start times and downtime information for each furnace.
 */
function getStartDict(
  monthList,
  furList,
  calendarData,
  length_recipe,
  furnaceName,
  furnaceRecipeData
) {
  const firstDate = new Date();

  const startDict = {};
  const filteredList = furList.filter(
    // obtains all of the processes for a specific furnace name
    (furnace) => furnace["furnace_name"] === furnaceName
  );
  for (let i = 0; i < filteredList.length; i++) {
    let values = [];
    // values[1] represents the end time of the process, based on if blocks are removed or if there is an abort.
    let date = new Date(filteredList[i]["start_time"]);

    const timeDifference = date - firstDate;

    const dayDifference = timeDifference / (1000 * 60 * 60 * 24);
    let furId = filteredList[i]["primary_id"];
    values.push(dayDifference); // values[0] is the index of the startDate relative to the first day in the calendar
    const abortList = calendarData.filter(
      // Obtains the aborts for that specific index. abort, power, and maintenance are lists due to previous misunderstanding
      // of behavior. Will probably have to change.
      (block) =>
        block.block === "Aborted" && block.furnace_id === furId.toString()
    );

    let abortValues = abortList.map((value) => value["sequence"]);

    const powerList = calendarData.filter(
      (block) =>
        block.block === "Down (Power)" && block.furnace_id === furId.toString()
    );
    let powerValues = powerList.map((value) => value["sequence"]);

    const maintenanceList = calendarData.filter(
      (block) =>
        block.block === "Down (Maintenance)" &&
        block.furnace_id === furId.toString()
    );
    let maintenanceValues = maintenanceList.map((value) => value["sequence"]);
    if (abortValues[0]) {
      values.push(abortValues[0] + 1); // pushes the abort index into values[1].
    } else if (maintenanceValues[0]) {
      values.push(maintenanceValues[0] + 1);
    } else if (powerValues[0]) {
      values.push(powerValues[0] + 1);
    } else {
      // otherwise just push the default end_time because there is no abort, or down
      let length_rec = calendarData.find(
        (value) => value["furnace_id"] === furId.toString()
      );

      if (length_rec && length_rec["end_time"]) {
        // makes sure to avoid end_time error.
        length_rec = length_rec["end_time"];
        values.push(length_rec);
      } else {
        values.push(null);
      }
    }
    startDict[furId] = values; // does it for each furnace
  }
  return startDict;
}
/**
 * Generates a list of months with their corresponding year and number of days, starting from the current month.
 * Current month just has the remaining days. Last month is the month before the current month, but next year.
 * @returns {Array<Object>} - An array of objects containing the month name, year, and the number of days in the month.
 */
function getMonthListWithYearAndDays() {
  const monthNames = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];

  const date = new Date();
  const currentMonthIndex = date.getMonth();
  const currentYear = date.getFullYear();

  const monthsWithYearAndDays = [];

  for (let i = 0; i < monthNames.length; i++) {
    const monthIndex = (currentMonthIndex + i) % 12;
    const year = monthIndex < currentMonthIndex ? currentYear + 1 : currentYear;
    const days = daysInMonth(monthIndex, year);
    if (i !== 0) {
      monthsWithYearAndDays.push({
        month: `${monthNames[monthIndex]} ${year}`,
        days: days.toString(),
      });
    } else {
      const curMonthDays = days - date.getDate() + 1;
      monthsWithYearAndDays.push({
        month: `${monthNames[monthIndex]} ${year}`,
        days: curMonthDays.toString(),
      });
    }
  }

  return monthsWithYearAndDays;
}

/**
 * SchedulerBlocks Component
 * Displays a table for scheduling furnace processes with block events.
 * Includes scrollable functionality and interaction with popovers for detailed block information.
 * @param {Object} props - The component props.
 * @param {number} props.furnaceNum - The number of furnaces.
 * @param {Array} props.furnaceData - The data for furnaces.
 * @param {Array} props.apiData - The data for recipes.
 * @param {Array} props.recipeList - The list of recipe names.
 * @param {Array} props.blockData - The data for blocks associated with furnaces.
 * @param {Array} props.colorData - The data for colors associated with blocks.
 * @param {Array} props.calendarData - The data for calendar events.
 * @param {Array} props.downData - The data for downtime events.
 * @param {Array} props.furnaceRecipeData - The data for furnace recipes.
 * @returns {JSX.Element} The rendered component.
 */
const SchedulerBlocks = ({
  furnaceNum,
  furnaceData,
  apiData,
  recipeList,
  blockData,
  colorData,
  calendarData,
  downData,
  furnaceRecipeData,
}) => {
  const monthList = getMonthListWithYearAndDays();

  let startDate = new Date();
  const year = startDate.getFullYear();

  const daysYear = daysInYear(year) - startDate.getDate();
  let endDate = addDays(startDate, daysYear - 1);
  let dates = getDate(startDate, endDate);
  let date_headers = dates.map((date) => date.getDate());

  const tableContainerRef = useRef(null);
  useEffect(() => {
    // handles scrolling in the horizontal direction
    const tableContainer = tableContainerRef.current;
    const handleWheel = (event) => {
      if (event.deltaY !== 0) {
        event.preventDefault();
        tableContainer.scrollLeft += event.deltaY;
      }
    };

    if (tableContainer) {
      tableContainer.addEventListener("wheel", handleWheel);
    }

    return () => {
      if (tableContainer) {
        tableContainer.removeEventListener("wheel", handleWheel);
      }
    };
  }, []);
  // obtains an object with the furnace data for each unique furnace
  const groupedFurnaceData = furnaceData.reduce((acc, row) => {
    const { furnace_name } = row;
    if (!acc[furnace_name]) {
      acc[furnace_name] = [];
    }
    acc[furnace_name].push(row);
    return acc;
  }, {});

  // finds if there is an ongoing process in that index.
  const findIdInRange = (index, startDict) => {
    return Object.keys(startDict).find(
      (id) =>
        index >= startDict[id][0] && index < startDict[id][0] + startDict[id][1]
    );
  };

  return (
    <figure className="table-container" ref={tableContainerRef}>
      <figure className="table-container-inner">
        <table className="schedule-table">
          <thead>
            <tr className="month-years">
              <td></td>
              <td></td>

              {monthList.map((month) => (
                <th
                  key={`${month.month}`}
                  className="month-year"
                  colSpan={month["days"]}
                >
                  {month["month"]}
                </th>
              ))}
            </tr>

            <tr className="day-columns">
              <th className="day-header-left">Furnace Names</th>
              <th className="day-header-right">Process Recipes</th>

              {date_headers.map((day, index) => (
                <th key={`day-${index}`} className="day">
                  {" "}
                  {day}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {Object.keys(groupedFurnaceData).map(
              (furnaceName, furnaceIndex) => {
                let killedDict = {};

                const processesWithFurnace =
                  groupedFurnaceData[furnaceName] || [];
                // Only contains processes with that furnaceName.
                // Creating the killedDict, which indicates if a process has been killed.

                processesWithFurnace.forEach((process) => {
                  killedDict[process["primary_id"]] = false;
                });
                // associates each process id with a boolean, false if it has not been killed, true if it has.
                let last;
                console.log(furnaceRecipeData);
                const matchFurName = furnaceRecipeData.find(
                  (furnace) => furnace["furnace"] === furnaceName // match is only used to find the length of the recipe
                );
                const recipe_name = matchFurName
                  ? matchFurName["recipe"]
                  : null;
                const id_length =
                  groupedFurnaceData[furnaceName][0]["primary_id"];

                const match = calendarData.find(
                  (calendar) => calendar.furnace_id === id_length.toString() // match is only used to find the length of the recipe, don't think it does anything right now.
                );

                let length_recipe;

                let emptyRow = false; // if the row is an empty newly added row
                if (groupedFurnaceData[furnaceName][0]["start_time"]) {
                  emptyRow = false; // Set to true if match["end_time"] is valid (not null or undefined)
                } else {
                  emptyRow = true; // Set to false if match["end_time"] is not valid
                }
                let startDict = {};
                if (!emptyRow) {
                  startDict = getStartDict(
                    monthList,
                    furnaceData,
                    calendarData,
                    length_recipe,
                    furnaceName
                  );
                }

                return (
                  <tr key={furnaceName}>
                    <th className="row-header-left">{furnaceName}</th>
                    <th className="row-header-right">{recipe_name}</th>
                    {date_headers.map((date, index) => {
                      let curId = parseInt(findIdInRange(index, startDict));
                      const maxId = Math.max(...Object.keys(startDict));
                      // curId is a string initially

                      if (curId) {
                        // checks if the index is in the range of a process
                        const blocks = calendarData.filter(
                          // filters out blocks for that recipe only.
                          (block) => block.furnace_id === curId.toString()
                        );

                        const curIndex = Math.floor(
                          // finds the index of the current block relative ot start date
                          index - startDict[curId][0]
                        );
                        let count = 0;
                        let cur = index - startDict[curId][0]; //don't remember why I did this twice but without floor.
                        let length_blocks = blocks.length;

                        let prev = 0;
                        let state = "Starting";
                        const abortList = calendarData.filter(
                          // same abort list and logic as before.
                          (block) =>
                            block.block === "Aborted" &&
                            block.furnace_id === curId.toString()
                        );

                        let abortValues = abortList.map(
                          (value) => value["sequence"]
                        );

                        const powerList = calendarData.filter(
                          (block) =>
                            block.block === "Down (Power)" &&
                            block.furnace_id === curId.toString()
                        );
                        let powerValues = powerList.map(
                          (value) => value["sequence"]
                        );

                        const maintenanceList = calendarData.filter(
                          (block) =>
                            block.block === "Down (Maintenance)" &&
                            block.furnace_id === curId.toString()
                        );
                        let maintenanceValues = maintenanceList.map(
                          (value) => value["sequence"]
                        );
                        let killed = false;
                        if (
                          // if there is an abort, power, or down value, set the row to killed.
                          abortValues.length +
                            powerValues.length +
                            maintenanceValues.length >
                          0
                        ) {
                          killed = true;
                        }

                        length_blocks -=
                          abortValues.length +
                          powerValues.length +
                          maintenanceValues.length; // changes the number of blocks based on if there are abort or down values.
                        let length_rec = startDict[curId][1]; // obtains the end time based on the startDict.
                        length_recipe = length_rec;
                        // This code iterates through a sequence of blocks to find which block the current position (`cur`) belongs to.
                        // It compares the current position to the range of each block (from `prev` to `next`), and when the correct block is found,
                        // it sets the `state` to the current block's state and exits the loop.
                        while (count < length_blocks) {
                          let next = 0;
                          if (count === length_blocks - 1) {
                            next = length_rec;
                          } else {
                            next = blocks[count + 1]["sequence"];
                          }

                          if (cur >= prev && cur <= next) {
                            state = blocks[count]["block"];

                            break;
                          } else {
                            prev = next;
                            count += 1;
                          }
                        }

                        let startValue = Math.floor(startDict[curId][0]);
                        if (
                          abortValues.includes(index - startValue - 1) &&
                          killedDict[curId] === false
                        ) {
                          killedDict[curId] = true;
                          if (curId === maxId) {
                            last = index + 1;
                          } // only include the block if the process has not been killed yet.
                          return (
                            <td
                              key={`filled-${furnaceIndex}-${index}`}
                              className="aborted-block"
                            >
                              <BasicPopover
                                name="Aborted"
                                idnum={curId}
                                state={state}
                                calendarData={calendarData}
                                curIndex={curIndex}
                                downData={downData}
                                killed={killed}
                              />
                            </td>
                          );
                        } else if (
                          powerValues.includes(index - startValue - 1) &&
                          killedDict[curId] === false
                        ) {
                          killedDict[curId] = true;
                          if (curId === maxId) {
                            last = index + 1;
                          }
                          return (
                            <td
                              key={`filled-${furnaceIndex}-${index}`}
                              className="power-block"
                            >
                              <BasicPopover
                                name="Down-Power"
                                idnum={curId}
                                state={state}
                                calendarData={calendarData}
                                curIndex={curIndex}
                                downData={downData}
                                killed={killed}
                              />
                            </td>
                          );
                        } else if (
                          maintenanceValues.includes(index - startValue - 1) &&
                          killedDict[curId] === false
                        ) {
                          killedDict[curId] = true;
                          if (curId === maxId) {
                            last = index + 1;
                          }
                          return (
                            <td
                              key={`filled-${furnaceIndex}-${index}`}
                              className="maintenance-block"
                            >
                              <BasicPopover
                                name="Down-Maintenance"
                                idnum={curId}
                                state={state}
                                calendarData={calendarData}
                                curIndex={curIndex}
                                downData={downData}
                                killed={killed}
                              />
                            </td>
                          );
                        }

                        if (
                          state === "Running" &&
                          killedDict[curId] === false
                        ) {
                          return (
                            <td
                              key={`filled-${furnaceIndex}-${index}`}
                              className="running-block"
                            >
                              {
                                <BasicPopover
                                  name={`${Math.round(cur) - prev}`}
                                  idnum={curId}
                                  state={state}
                                  calendarData={calendarData}
                                  curIndex={curIndex}
                                  downData={downData}
                                  killed={killed}
                                ></BasicPopover>
                              }
                            </td>
                          );
                        } else if (
                          state === "Finishing" &&
                          killedDict[curId] === false
                        ) {
                          let temp = blocks[count - 1]["sequence"];

                          return (
                            <td
                              key={`filled-${furnaceIndex}-${index}`}
                              className="finishing-block"
                            >
                              {" "}
                              {
                                <BasicPopover
                                  name={`${state}${Math.round(cur) - temp}`}
                                  idnum={curId}
                                  state={state}
                                  calendarData={calendarData}
                                  curIndex={curIndex}
                                  downData={downData}
                                  killed={killed}
                                ></BasicPopover>
                              }
                            </td>
                          );
                        } else if (
                          state === "Preparing" &&
                          killedDict[curId] === false
                        ) {
                          return (
                            <td
                              key={`filled-${furnaceIndex}-${index}`}
                              className="preparing-block"
                            >
                              {" "}
                              {
                                <BasicPopover
                                  name={`${state}${Math.round(cur) - prev}`}
                                  idnum={curId}
                                  state={state}
                                  calendarData={calendarData}
                                  curIndex={curIndex}
                                  downData={downData}
                                  killed={killed}
                                ></BasicPopover>
                              }{" "}
                            </td>
                          );
                        } else if (
                          state === "Starting" &&
                          killedDict[curId] === false
                        ) {
                          return (
                            <td
                              key={`filled-${furnaceIndex}-${index}`}
                              className="starting-block"
                            >
                              {" "}
                              {
                                <BasicPopover
                                  name={`${state}${Math.round(cur) - prev}`}
                                  idnum={curId}
                                  state={state}
                                  calendarData={calendarData}
                                  curIndex={curIndex}
                                  downData={downData}
                                  killed={killed}
                                ></BasicPopover>
                              }
                            </td>
                          );
                        }
                      }
                      let startDay = new Date();
                      const currentDate = addDays(startDay, index);

                      // makes sure to add the block to the dropdown in the proper format.
                      const formatDate = (date) => {
                        const month = (date.getMonth() + 1)
                          .toString()
                          .padStart(2, "0"); // getMonth() is zero-based
                        const day = date.getDate().toString().padStart(2, "0");
                        const year = date.getFullYear();
                        return `${year}-${month}-${day}`;
                      };

                      const formattedDate = formatDate(currentDate);
                      curId = parseInt(
                        findIdInRange(index - 1, startDict, length_recipe)
                      );

                      if (curId === maxId && killedDict[curId] === false) {
                        last = Math.ceil(startDict[curId][0] + length_recipe);
                      }

                      if (index === last || emptyRow === true) {
                        return (
                          <td
                            key={`filled-${furnaceIndex}-${index}`}
                            className="empty-popover-calendar-day"
                          >
                            <PopoverForm
                              recipe={recipe_name}
                              furnaceName={furnaceName}
                              date={formattedDate}
                              apiData={apiData}
                              furnaceData={furnaceData}
                              blockData={blockData}
                              emptyRow={emptyRow}
                            />
                          </td>
                        );
                      } else {
                        return (
                          <td
                            key={`filled-${furnaceIndex}-${index}`}
                            className="empty-calendar-day"
                          ></td>
                        );
                      }
                    })}
                  </tr>
                );
              }
            )}
          </tbody>
        </table>
      </figure>
    </figure>
  );
};
export default SchedulerBlocks;
