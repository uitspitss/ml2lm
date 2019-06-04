const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const BrowserSyncPlugin = require('browser-sync-webpack-plugin');

module.exports = (env, argv) => ({
  mode: 'development',
  entry: './src/index.tsx',
  output: {
    path: path.resolve('../../src/static/frontend'),
    filename: 'main-[hash].js',
    publicPath: argv.mode === 'production' ? '' : 'http://localhost:3000/static/frontend/',
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: 'babel-loader',
      },
      {
        test: /\.tsx?$/,
        exclude: /node_modules/,
        use: 'ts-loader',
      },
    ],
  },
  resolve: {
    extensions: ['.ts', '.tsx', '.js', '.jsx'],
  },
  devServer: {
    hot: true,
    inline: true,
    port: 3000,
    headers: {
      'Access-Control-Allow-Origin': '*',
    },
  },
  plugins: [
    new BundleTracker({
      filename: argv.mode === 'production' ? './webpack-stats.json' : '../../tmp/webpack-stats.json'
    }),
  ],
});
