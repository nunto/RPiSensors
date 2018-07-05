import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { Menu, Segment } from 'semantic-ui-react';

class NavBar extends Component {
    constructor(props) {
        super(props);
        this.state = {activeItem: 'home'}
    }
    
    _handleItemClick = (e, { name }) => {
        console.log("Active: " + name)
        this.setState({ activeItem: name }) 
    }

    render() {
        const { activeItem } = this.state
        return (
                <div>
                    <Menu pointing secondary>
                        <Menu.Item name="home" active={activeItem === 'home'} onClick={this._handleItemClick} />
                        <Menu.Item name="devices" active={activeItem === 'devices'} onClick={this._handleItemClick} />
                        <Menu.Item name="sensors" active={activeItem === 'sensors'} onClick={this._handleItemClick} />
                    </Menu>
                </div>
        )
    }
}

export default NavBar;