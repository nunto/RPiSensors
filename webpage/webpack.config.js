const path = require('path');
const SRC_DIR = path.join(__dirname, '/react-client/src');
const DIST_DIR = path.join(__dirname, '/react-client/dist');
const webpack = require('webpack');
module.exports = {
  entry: `${SRC_DIR}/index.jsx`,
  output: {
    path: DIST_DIR,
    filename: 'bundle.js',
  },
  resolve: {
    extensions: ['.js', '.jsx', '.json', '.css']
  },
  module : {
    rules : [
      {
        test: /\.css$/,
        loader: 'style-loader!css-loader'
      },
      {
        test: /\.png$/,
        loader: 'url-loader?limit=100000&minetype=image/png'
      },
      {
        test: /\.jpg/,
        loader: 'file-loader'
      },
      {
        test : /\.jsx?$/,
        include : SRC_DIR,
        use: {
            loader : 'babel-loader',
            options: {
                presets: ['react', 'es2015', 'stage-0'],
                plugins: ["transform-es2015-destructuring", "transform-object-rest-spread"]
            }
        }
      }
    ]
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify('production')
    })
  ]
};