import { Paper, InputBase, IconButton } from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import CloseIcon from "@mui/icons-material/Close";

const SearchBar = ({ value, handleChange, handleSearch, handleClear }) => {
  return (
    <Paper
      sx={{
        p: "2px 4px",
        display: "flex",
        alignItems: "center",
        flexGrow: 1,
      }}
    >
      <InputBase
        sx={{ ml: 1, flex: 1 }}
        placeholder="粘贴漫画网址或搜索漫画"
        inputProps={{ "aria-label": "Search Bilibili Mangas" }}
        value={value}
        onChange={handleChange}
        onKeyDown={(event) => {
          if (event.code === "Enter") {
            handleSearch();
          }
        }}
      />
      {value !== "" && (
        <IconButton
          type="button"
          size="small"
          sx={{ marginRight: 1 }}
          aria-label="clear"
          onClick={handleClear}
        >
          <CloseIcon />
        </IconButton>
      )}
      <IconButton
        type="button"
        sx={{ p: "10px" }}
        aria-label="search"
        onClick={handleSearch}
      >
        <SearchIcon />
      </IconButton>
    </Paper>
  );
};

export default SearchBar;
