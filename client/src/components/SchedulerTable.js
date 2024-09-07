import SchedulerBlocks from "./SchedulerBlocks";
/**
 * SchedulerTable Component
 * Acts as a container for the SchedulerBlocks component.
 * It passes various data related to recipes, furnaces, blocks, colors, calendar events, and down reasons as props to the SchedulerBlocks component.
 * @param {Object} props - The component props.
 * @param {Array} props.apiData - List of recipes.
 * @param {Array} props.recipeList - List of recipe names.
 * @param {Array} props.furnaceData - List of furnace process information.
 * @param {Array} props.blockData - Block data associated with recipes.
 * @param {Array} props.colorData - Color data for visual representation.
 * @param {Array} props.calendarData - Calendar data for scheduling.
 * @param {Array} props.downData - Data for downtime reasons.
 * @param {Array} props.furnaceRecipeData - Furnace and recipe association data.
 * @returns {JSX.Element} The rendered component.
 */
const SchedulerTable = ({
  apiData,
  recipeList,
  furnaceData,
  blockData,
  colorData,
  calendarData,
  downData,
  furnaceRecipeData,
}) => {
  return (
    <div className="calendar-body">
      <SchedulerBlocks
        furnaceNum={furnaceData.length}
        furnaceData={furnaceData}
        apiData={apiData}
        recipeList={recipeList}
        blockData={blockData}
        colorData={colorData}
        calendarData={calendarData}
        downData={downData}
        furnaceRecipeData={furnaceRecipeData}
      />
    </div>
  );
};
export default SchedulerTable;
