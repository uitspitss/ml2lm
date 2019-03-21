import * as React from 'react';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';

import Form from './Form';
import Table from './Table';

const App = () => (
  <React.Fragment>
    <AppBar position="static">
      <Toolbar>
        <Typography variant="title" color="inherit">
          ML2LM
        </Typography>
      </Toolbar>
    </AppBar>

    <Grid container justify="center">
      <Grid item>
        <Form />
      </Grid>
      <Grid item>
        <Table />
      </Grid>
    </Grid>
  </React.Fragment>
);

export default App;
