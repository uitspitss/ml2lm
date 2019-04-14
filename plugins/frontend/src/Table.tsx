import * as React from 'react';
import { graphql } from 'react-apollo';
import gql from 'graphql-tag';

import Grid from '@material-ui/core/Grid';
import GridList from '@material-ui/core/GridList';
import GridListTile from '@material-ui/core/GridListTile';
import GridListTileBar from '@material-ui/core/GridListTileBar';
import LinearProgress from '@material-ui/core/LinearProgress';

interface Playlist {
  short_id: string;
  url: string;
  title: string;
  count: number;
  thumbnail_url: string;
}

const query = gql`
  query playlists {
    playlists @rest(type: "Playlists", path: "playlist/") {
      short_id
      url
      title
      count
      thumbnail_url
    }
  }
`;

const Table: React.FC<any> = ({ data: { loading, playlists } }) => {
  // TODO: 出ていないかも、チェック必要
  if (loading) {
    return <LinearProgress />;
  }

  return (
    <Grid container justify="center" alignItems="center">
      <Grid item xs={12}>
        <GridList cols={3} key="table">
          {playlists &&
            playlists.map((pl: Playlist) => (
              <GridListTile key={pl.short_id}>
                <img src={pl.thumbnail_url} />
                <a href={`${pl.short_id}`}>
                  <GridListTileBar title={pl.title} titlePosition="top" />
                </a>
              </GridListTile>
            ))}
        </GridList>
      </Grid>
    </Grid>
  );
};

export default graphql(query)(Table);
