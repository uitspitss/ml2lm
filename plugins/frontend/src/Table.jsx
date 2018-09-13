import React, { Component } from 'react';
import GridList from '@material-ui/core/GridList';
import GridListTile from '@material-ui/core/GridListTile';
import GridListTileBar from '@material-ui/core/GridListTileBar';
import IconButton from '@material-ui/core/IconButton';
import StarBorderIcon from '@material-ui/icons/StarBorder';
import Grid from '@material-ui/core/Grid';


export default class Table extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      loaded: false
    }
  }

  componentDidMount() {
    fetch(this.props.endpoint)
    .then(response => {
      if (response.status !== 200) {
        return this.setState({placeholder: "Something went wrong"});
      }
      return response.json();
    })
    .then(data => this.setState({data: data, loaded: true}));
  }

  render() {
    const data = this.state.data;
    return (
      <div>
        <Grid container justify="space-around" alignItems="center">
          <Grid item xs={12} md={9} lg={6}>
            <h3>shorten playlists</h3>
            <GridList cols={3}>
              {data.map(tile => (
                <GridListTile key={tile.short_id}>
                  <img src={tile.thumbnail_url} />
                  <GridListTileBar
                    title={tile.title}
                    titlePosition="top"
                  />
                </GridListTile>
              ))}
            </GridList>
          </Grid>
        </Grid>
      </div>
    );
  }
}
