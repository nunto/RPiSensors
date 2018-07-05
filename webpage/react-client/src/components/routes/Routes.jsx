import React, { Component } from 'react';
import { Route, Switch } from 'react-router-dom';
import HomePage from '../HomePage';
import Devices from '../Devices';
import Sensors from '../Sensors';

const Routes = () => (
    <Switch>
        <Route exact path='/' component={HomePage} />
        <Route path='/devices' component={Devices} />
        <Route path='/sensors' component={Sensors} />
    </Switch>
)

export default Routes;