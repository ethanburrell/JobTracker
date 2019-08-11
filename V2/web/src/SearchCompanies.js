
import Button from '@material-ui/core/Button';
import React from 'react';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import IconButton from '@material-ui/core/IconButton';
import Typography from '@material-ui/core/Typography';
import InputBase from '@material-ui/core/InputBase';
import { fade, makeStyles } from '@material-ui/core/styles';
import MenuIcon from '@material-ui/icons/Menu';
import SearchIcon from '@material-ui/icons/Search';
import TextField from '@material-ui/core/TextField';
import SearchBar from 'material-ui-search-bar'
import Box from '@material-ui/core/Box';
import SearchAppBar from "./NavBar.js"


class SearchCompanies extends React.Component {

render() {
  return (
    <div>
    <SearchAppBar />
    <Box m={2} />
    <SearchBar
          onChange={() => console.log('onChange')}
          onRequestSearch={() => console.log('onRequestSearch')}
          style={{
            margin: '0 auto',
            maxWidth: 800
          }}
        />
     </div>
  )
}
}

export default SearchCompanies;
