import React, { Component } from 'react';
import { Feed, Icon } from 'semantic-ui-react';
import "./style/Home.css";
import Dash from './dashboard/Dashboard';

// Renders the Dashboard
class HomePage extends Component {
    render () {
        return (
            <Dash />
        )
    }
}

export default HomePage;
