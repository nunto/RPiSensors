import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import NavBar from './header/NavBar';
import Routes from './routes/Routes'

// Renders the Navigation Bar and Routes components -> See ./routes/Routes.jsx and ./header/Navbar
const App = () => (
    <div>
        <NavBar />
        <Routes />
    </div>
)

export default App;