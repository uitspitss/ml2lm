import * as React from 'react';
import { withFormik, InjectedFormikProps } from 'formik';
import * as Yup from 'yup';
import { Query, Mutation } from 'react-apollo';
import gql from 'graphql-tag';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
// import CircularProgress from '@material-ui/core/CircularProgress';
import GridList from '@material-ui/core/GridList';
import GridListTile from '@material-ui/core/GridListTile';
import GridListTileBar from '@material-ui/core/GridListTileBar';

// axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';
// axios.defaults.xsrfCookieName = 'csrftoken';

const CHECK_PLAYLIST_URL = gql`
  query checkPlaylistUrl($url: string!) {
    playlists(url: $url)
      @rest(type: "[Playlist]", path: "playlist/?url={args.url}") {
      short_id
      url
      title
      count
      thumbnail_url
    }
  }
`;

const POST_PLAYLIST_URL = gql`
  mutation postPlaylistUrl($url: string!) {
    postPlaylist(input: { url: $url })
      @rest(type: "Playlist", path: "playlist/", method: "POST") {
      short_id
      url
      title
      count
      thumbnail_url
    }
  }
`;

interface FormValues {
  url: string;
}

const Form: React.FC<InjectedFormikProps<{}, FormValues>> = ({
  touched,
  errors,
  values,
  isSubmitting,
  isValid,
  handleSubmit,
  handleChange,
}) => {
  return (
    <Query
      query={CHECK_PLAYLIST_URL}
      variables={{ url: values.url }}
      skip={!values.url}
      pollInterval={1000}
    >
      {({ data, loading }) => (
        <Grid
          container
          direction="column"
          justify="space-between"
          alignItems="center"
        >
          <Grid item xs={9}>
            <Mutation mutation={POST_PLAYLIST_URL} key="post">
              {postPlaylist => (
                <form
                  encType="multipart/form-data"
                  onSubmit={(e: any) => {
                    e.preventDefault();
                    postPlaylist({ variables: { url: values.url } });
                  }}
                >
                  <Grid container direction="row" justify="center">
                    <Grid item style={{ margin: 10 }}>
                      <TextField
                        name="url"
                        value={values.url}
                        onChange={handleChange}
                        label="shorten playlist url"
                        placeholder="shorten url"
                        style={{ width: '50vw' }}
                      />
                    </Grid>
                    <Grid item style={{ margin: 10 }}>
                      <Button
                        type="submit"
                        variant="contained"
                        disabled={!isValid || isSubmitting}
                        color="primary"
                      >
                        shorten
                      </Button>
                    </Grid>
                  </Grid>
                </form>
              )}
            </Mutation>
          </Grid>
          <Grid item xs={6} style={{ margin: 10 }}>
            <TextField
              label="shorten playlist url"
              value={
                data && data.playlists && data.playlists.length
                  ? `${location.protocol}//${location.host}/${
                      data.playlists[0].short_id
                    }`
                  : ''
              }
              placeholder="shorten url"
              style={{ width: '30vw' }}
              InputLabelProps={{ shrink: true }}
            />
          </Grid>
          <Grid item xs={6} style={{ margin: 20 }}>
            {data &&
              data.playlists &&
              data.playlists.map((pl: any) => (
                <GridList cols={1} key="shorten">
                  <GridListTile key={`shorten_${pl.short_id}`}>
                    <img src={pl.thumbnail_url} />
                    <a href={`${pl.short_id}`}>
                      <GridListTileBar title={pl.title} titlePosition="top" />
                    </a>
                  </GridListTile>
                </GridList>
              ))}
          </Grid>
        </Grid>
      )}
    </Query>
  );
};

export default withFormik({
  mapPropsToValues: () => ({ url: '' }),
  validationSchema: Yup.object().shape({
    url: Yup.string().required('Required'),
  }),
  handleSubmit: (values, { setSubmitting }) => {},
})(Form);

// export default class Form extends Component {
//   constructor(props) {
//     super(props);
//     this.handleCheckUrl = this.handleCheckUrl.bind(this);
//     this.handlePostUrl = this.handlePostUrl.bind(this);
//     this.state = {
//       url: '',
//       shortenedUrl: '',
//       shortenedTitle: '',
//       thumbnailUrl: '',
//       disablePost: true,
//       shortenSuccess: false,
//     };
//   }

//   handleCheckUrl(event) {
//     const url = event.target.value.replace(/watch\?v=.*&/g, 'playlist?');
//     this.setState(
//       {
//         url: url,
//         shortenedUrl: '',
//       },
//       () => {
//         axios
//           .get(`${this.props.endpoint}?url=${url}`)
//           .then(response => {
//             if (response.status !== 200) {
//               console.error('handleCheckUrl');
//             }
//             return response.data;
//           })
//           .then(data => {
//             if (data.length) {
//               this.setState({
//                 shortenedUrl: `${location.protocol}//${location.host}/${
//                   data[0].short_id
//                 }`,
//                 disablePost: true,
//               });
//             } else {
//               if (this.state.url === '') {
//                 this.setState({
//                   disablePost: true,
//                   shortenedUrl: '',
//                   shortenedTitle: '',
//                   thumbnailUrl: '',
//                   shortenSuccess: false,
//                 });
//               } else {
//                 this.setState({ disablePost: false });
//               }
//             }
//           });
//       },
//     );
//   }

//   handlePostUrl(event) {
//     axios
//       .post(this.props.endpoint, {
//         url: this.state.url,
//       })
//       .then(response => {
//         if (response.status !== 201) {
//           console.error('handlePostUrl');
//         }
//         return response.data;
//       })
//       .then(data => {
//         this.setState({
//           disablePost: true,
//           shortenedUrl: `${location.protocol}//${location.host}/${
//             data.short_id
//           }`,
//           shortenedTitle: data.title,
//           thumbnailUrl: data.thumbnail_url,
//           shortenSuccess: true,
//         });
//       });
//   }

//   render() {
//     return (
//       <div>
//         <Grid container justify="space-around" alignItems="center">
//           <Grid item>
//             <form className="main_form">
//               <TextField
//                 id="url"
//                 label="playlist url"
//                 placeholder="http://xxxxx"
//                 style={{ width: '500px' }}
//                 onChange={this.handleCheckUrl}
//                 margin="normal"
//               />
//             </form>
//           </Grid>
//         </Grid>

//         <Grid container justify="space-around" alignItems="center">
//           <Grid item>
//             <Button
//               variant="contained"
//               color="primary"
//               disabled={this.state.disablePost}
//               onClick={this.handlePostUrl}
//             >
//               shorten
//             </Button>
//           </Grid>
//         </Grid>

//         <Grid container justify="space-around" alignItems="center">
//           <Grid item>
//             <TextField
//               label="shorten playlist url"
//               value={this.state.shortenedUrl}
//               placeholder="shorten url"
//               style={{ width: '300px' }}
//               margin="normal"
//             />
//           </Grid>
//         </Grid>

//         <Grid
//           container
//           justify="space-around"
//           alignItems="center"
//           style={{ display: this.state.shortenSuccess ? '' : 'none' }}
//         >
//           <GridList cols={1} style={{ width: '300px' }}>
//             <GridListTile>
//               <img src={this.state.thumbnailUrl} />
//               <a href={this.state.shortenedUrl}>
//                 <GridListTileBar
//                   title={this.state.shortenedTitle}
//                   titlePosition="top"
//                 />
//               </a>
//             </GridListTile>
//           </GridList>
//         </Grid>
//       </div>
//     );
//   }
// }
