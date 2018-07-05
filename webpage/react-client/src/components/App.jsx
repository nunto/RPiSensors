import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import NavBar from './header/NavBar';
import Routes from './routes/Routes'

const App = () => (
    <div>
        <NavBar />
        <Routes />
    </div>
)
/**
class App extends Component {
    render() {
        return (
            <div>
                <NavBar />
                <Routes />
                <Route name="home" exact path ="/" component={HomePage} />
            </div>
        )
    }
}
*/
export default App;