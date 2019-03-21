import * as React from 'react';
import { ApolloClient } from 'apollo-client';
import { InMemoryCache } from 'apollo-cache-inmemory';
import { RestLink } from 'apollo-link-rest';
import gql from 'graphql-tag';

// import GridList from '@material-ui/core/GridList';
// import GridListTile from '@material-ui/core/GridListTile';
// import GridListTileBar from '@material-ui/core/GridListTileBar';
// import IconButton from '@material-ui/core/IconButton';
// import InfoIcon from '@material-ui/icons/Info';
// import Grid from '@material-ui/core/Grid';

const restLink = new RestLink({ uri: 'api/' });

const client = new ApolloClient({
  link: restLink,
  cache: new InMemoryCache(),
});

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

client.query({ query }).then(res => {
  console.log(res.data);
});

const Table: React.FC<{}> = () => {
  return (
    <React.Fragment>
      <div className="table">dttable</div>
    </React.Fragment>
  );
};

export default Table;
// export default class Table extends Component {
//   constructor(props) {
//     super(props);
//     this.state = {
//       data: [],
//       loaded: false
//     }
//   }

//   componentDidMount() {
//     axios.get(this.props.endpoint)
//     .then(response => {
//       if (response.status !== 200) {
//         return this.setState({placeholder: "Something went wrong"});
//       }
//       return response.data;
//     })
//     .then(data => this.setState({data: data, loaded: true}));
//   }

//   render() {
//     const data = this.state.data;
//     return (
//       <div>
//         <Grid container justify="space-around" alignItems="center">
//           <Grid item xs={12} md={9} lg={6}>
//             <h3>shortened playlists</h3>
//             <GridList cols={3}>
//               {data.map(tile => (
//                 <GridListTile key={tile.short_id}>
//                   <img src={tile.thumbnail_url} />
//                   <a href={`${location.protocol}//${location.host}/${tile.short_id}`}>
//                     <GridListTileBar
//                       title={tile.title}
//                       titlePosition="top"
//                     />
//                   </a>
//                 </GridListTile>
//               ))}
//             </GridList>
//           </Grid>
//         </Grid>
//       </div>
//     );
//   }
// }
