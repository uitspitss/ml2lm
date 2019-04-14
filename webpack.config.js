const BundleTracker = require('webpack-bundle-tracker');
const BrowserSyncPlugin = require('browser-sync-webpack-plugin');

module.exports = {
  mode: 'development',
  entry: './plugins/frontend/src/index.tsx',
  output: {
    path: `${__dirname}/plugins/frontend/static/frontend`,
    filename: 'main.js',
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
  plugins: [
    new BundleTracker({ filename: './plugins/frontend/webpack-stats.json' }),
    new BrowserSyncPlugin({
      host: 'localhost',
      port: 8000,
      proxy: 'http://localhost:8000/',
    }),
  ],
};
