import "./App.css";
import API from "./api";
//import RecipeTable from "./components/RecipeTable.js";

import DynamicTable from "./components/DynamicTable.js";
import FurnaceTable from "./components/FurnaceTable.js";
import SchedulerTable from "./components/SchedulerTable.js";
import PersistentDrawerLeft from "./components/PersistentDrawerLeft.js";

import { Route, Routes } from "react-router-dom";
import { useEffect, useState } from "react";

/**
 * Main component of the application that sets up routes and manages data fetching from the API.
 * @returns {JSX.Element} The rendered component.
 */
function App() {
  const [apiResponse, setApiResponse] = useState([]);
  const [furnaceResponse, setfurnaceResponse] = useState([]);
  const [calendarResponse, setCalendarResponse] = useState([]);
  const [blockResponse, setBlockResponse] = useState([]);
  const [colorResponse, setColorResponse] = useState([]);
  const [downResponse, setDownResponse] = useState([]);
  const [furnaceRecipeResponse, setfurnaceRecipeResponse] = useState([]);
  /**
   * useEffect hook to fetch data from the API when the component mounts.
   * Multiple API calls are made to retrieve data for recipes, furnace recipes,
   * blocks, colors, calendar, down reasons, and furnaces.
   */
  useEffect(() => {
    // Gets the recipe_table from the database
    API({
      method: "GET",
      url: "/api/recipes",
    }).then((response) => {
      const res = response.data;
      setApiResponse(res);
    });
    API({
      // Gets the furnace_recipe_table from the database
      method: "GET",
      url: "/api/furnaceRecipes",
    }).then((response) => {
      const res = response.data;
      setfurnaceRecipeResponse(res);
    });
    API({
      // Gets the furnace_recipe_table from the database
      method: "GET",
      url: "/api/blocks",
    }).then((response) => {
      const res = response.data;
      setBlockResponse(res);
    });
    API({
      // Gets the color_table from the database
      method: "GET",
      url: "/api/colors",
    }).then((response) => {
      const res = response.data;
      setColorResponse(res);
    });
    API({
      // Gets the calendar_table from the database
      method: "GET",
      url: "/api/calendar",
    }).then((response) => {
      const res = response.data;
      setCalendarResponse(res);
    });
    API({
      // Gets the downreasons_table from the database
      method: "GET",
      url: "/api/downreasons",
    }).then((response) => {
      const res = response.data;
      setDownResponse(res);
    });
    API({
      //Gets the furnaces_table from the database
      method: "GET",
      url: "/api/furnaces",
    }).then((response) => {
      const res = response.data;
      setfurnaceResponse(res);
    });
  }, []);
  const recipeNames = furnaceResponse.map((recipe) => recipe.recipe_key); // obtain the unique recipe names list
  return (
    <Routes>
      <Route
        path="/furnaces"
        element={
          <header className="App-header">
            <PersistentDrawerLeft pageSwitch={"/"}></PersistentDrawerLeft>
            <DynamicTable
              jsonData={apiResponse}
              recipeList={recipeNames}
              blockData={blockResponse}
              colorData={colorResponse}
            />
            <FurnaceTable
              apiData={apiResponse}
              furnaceData={furnaceResponse}
              blockData={blockResponse}
              furnaceRecipeData={furnaceRecipeResponse}
            />
          </header>
        }
      />
      <Route
        path="/"
        element={
          <div>
            <PersistentDrawerLeft
              pageSwitch={"/furnaces"}
            ></PersistentDrawerLeft>
            <SchedulerTable
              apiData={apiResponse}
              recipeList={recipeNames}
              furnaceData={furnaceResponse}
              blockData={blockResponse}
              colorData={colorResponse}
              calendarData={calendarResponse}
              downData={downResponse}
              furnaceRecipeData={furnaceRecipeResponse}
            />{" "}
          </div>
        }
      />
    </Routes>
  );
}

export default App;
