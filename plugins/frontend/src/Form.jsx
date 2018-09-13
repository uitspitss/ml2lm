import React, { Component } from 'react';
import axios from 'axios';
import MenuItem from '@material-ui/core/MenuItem';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Icon from '@material-ui/core/Icon';
import Grid from '@material-ui/core/Grid';
import FileCopy from '@material-ui/icons/FileCopy';
import GridList from '@material-ui/core/GridList';
import GridListTile from '@material-ui/core/GridListTile';
import GridListTileBar from '@material-ui/core/GridListTileBar';

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export default class Form extends Component {
  constructor(props) {
    super(props);
    this.handleCheckUrl = this.handleCheckUrl.bind(this);
    this.handlePostUrl = this.handlePostUrl.bind(this);
    this.state = {
      url: '',
      shortenUrl: '',
      shortenTitle: '',
      thumbnailUrl: '',
      disablePost: true,
      shortenSuccess: false,
    };
  }

  handleCheckUrl(event) {
    const url = event.target.value.replace(/watch\?v=.*&/g, 'playlist?');
    this.setState(
      {
        url: url,
        shortenUrl: ''
      },
      () => {
        axios.get(`${this.props.endpoint}?url=${url}`)
        .then(response => {
          if (response.status !== 200) {
            console.error('handleCheckUrl');
          }
          return response.data;
        })
        .then(data => {
          if(data.length){
            this.setState({
              shortenUrl: `${location.protocol}//${location.host}/${data[0].short_id}`,
              disablePost: true
            });
          } else {
            if(this.state.url === '') {
              this.setState({
                disablePost: true,
                shortenUrl: '',
                shortenTitle: '',
                thumbnailUrl: '',
                shortenSuccess: false,
              });
            } else {
              this.setState({disablePost: false});
            }
          }
        })
      }
    );
  }

  handlePostUrl(event) {
    axios.post(
      this.props.endpoint,
      {
        url: this.state.url
      }
    )
    .then(response => {
      if (response.status !== 201) {
        console.error('handlePostUrl');
      }
      return response.data;
    })
    .then(data => {
      this.setState({
        disablePost: true,
        shortenUrl: `${location.protocol}//${location.host}/${data.short_id}`,
        shortenTitle: data.title,
        thumbnailUrl: data.thumbnail_url,
        shortenSuccess: true,
      });
    });
  }

  render() {
    return (
      <div>
        <Grid container justify="space-around" alignItems="center">
          <Grid item>
            <form className="main_form">
              <TextField
                id="url"
                label="playlist url"
                placeholder="http://xxxxx"
                style={{ width: '500px' }}
                onChange={this.handleCheckUrl}
                margin="normal"
              />
            </form>
          </Grid>
        </Grid>

        <Grid container justify="space-around" alignItems="center">
          <Grid item>
            <Button
              variant="contained"
              color="primary"
              disabled={this.state.disablePost}
              onClick={this.handlePostUrl}
            >
              shorten
            </Button>
          </Grid>
        </Grid>

        <Grid container justify="space-around" alignItems="center">
          <Grid item>
            <TextField
              label="shorten playlist url"
              value={this.state.shortenUrl}
              placeholder="shorten url"
              style={{ width: '300px' }}
              margin="normal"
            />
          </Grid>
        </Grid>

        <Grid container
          justify="space-around"
          alignItems="center"
          style={{ display: this.state.shortenSuccess? '' : 'none' }}
        >
          <GridList cols={1} style={{ width: '300px' }}>
            <GridListTile>
              <img src={this.state.thumbnailUrl} />
              <GridListTileBar
                title={this.state.shortenTitle}
                titlePosition="top"
              />
            </GridListTile>
          </GridList>
        </Grid>

      </div>
    );
  }
}
