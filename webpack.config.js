const CleanWebpackPlugin = require('clean-webpack-plugin');
const BundleTracker = require('webpack-bundle-tracker');
const BrowserSyncPlugin = require('browser-sync-webpack-plugin');

module.exports = {
  mode: 'development',
  entry: './plugins/frontend/src/index.jsx',
  output: {
    path: `${__dirname}/plugins/frontend/static/frontend`,
    filename: 'main-[hash].js'
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: [
          {
            loader: 'babel-loader',
            options: {
              presets: [
                ['env', {'modules': false}],
                'react'
              ]
            }
          }
        ]
      }
    ]
  },
  resolve: {
    extensions: [
      '.js', '.jsx',
    ]
  },
  plugins: [
    new BundleTracker({filename: './plugins/frontend/webpack-stats.json'}),
    new BrowserSyncPlugin({
        host: 'localhost',
        port: 8000,
        proxy: 'http://localhost:8000/'
    }),
    new CleanWebpackPlugin(
      ['./plugins/frontend/static/frontend/*.js'],
    ),
  ]
};
