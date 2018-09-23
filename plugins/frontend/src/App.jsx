import React, { Component } from 'react';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';

import Form from './Form';
import Table from './Table';


const App = () => (
  <div className="App">
    <AppBar position="static">
      <Toolbar>
        <Typography variant="title" color="inherit">
          ML2LM
        </Typography>
      </Toolbar>
    </AppBar>

    <Form endpoint='api/playlist/' />

    <Table endpoint='api/playlist/' />
  </div>
);

export default App;
