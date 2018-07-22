const CleanWebpackPlugin = require('clean-webpack-plugin');
const BundleTracker = require('webpack-bundle-tracker');

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
        test: /\.jsx$/,
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
  plugins: [
    new CleanWebpackPlugin(['./plugins/frontend/static/frontend/*.js']),
    new BundleTracker({filename: './webpack-stats.json'})
  ]
};
