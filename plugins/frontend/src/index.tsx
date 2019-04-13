import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { ApolloProvider } from 'react-apollo';
import { ApolloClient } from 'apollo-client';
import { InMemoryCache } from 'apollo-cache-inmemory';
import { RestLink } from 'apollo-link-rest';
import { ApolloLink, concat } from 'apollo-link';
import Cookies from 'universal-cookie';

import App from './App';

const cookies = new Cookies();

const restLink = new RestLink({ uri: 'api/', credentials: 'same-origin' });

const authMiddleware = new ApolloLink((operation, forward) => {
  operation.setContext({
    headers: {
      'X-CSRFToken': cookies.get('csrftoken'),
    },
  });
  return forward ? forward(operation) : null;
});

const client = new ApolloClient({
  link: concat(authMiddleware, restLink),
  cache: new InMemoryCache(),
});

ReactDOM.render(
  <ApolloProvider client={client}>
    <App />
  </ApolloProvider>,
  document.getElementById('root'),
);
