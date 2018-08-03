import React, { Component } from 'react';
import { Feed, Icon } from 'semantic-ui-react';
import "./style/Home.css";
import TemperatureChart from './widgets/TemperatureChart';


class HomePage extends Component {
    render () {
        return (
            <TemperatureChart />
        )
    }
}

export default HomePage;
