//import JsonData from '../../flask-server/config_files/recipes.json'
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from "@mui/material";
const RecipeTable = ({ jsonData }) => {
  //console.log(JsonData)

  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell align="right">Time (hrs)</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {jsonData.map((recipe) => (
            <TableRow
              key={recipe.time}
              sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
            >
              <TableCell component="th" scope="row">
                {recipe.recipe_name}
              </TableCell>
              <TableCell align="right">{recipe.time}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default RecipeTable;
