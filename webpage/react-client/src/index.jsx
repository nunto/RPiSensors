import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import 'babel-polyfill';
import App from './components/App';

ReactDOM.render((
    <Router>
        <App />
    </Router> 
), document.getElementById('app'))