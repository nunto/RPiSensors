import React, { Component } from 'react';
import { NavLink } from 'react-router-dom';
import { Menu, Segment } from 'semantic-ui-react';

class NavBar extends Component {
    constructor(props) {
        super(props);
        this.state = {activeItem: 'home'}
    }
    
    _handleItemClick = (e, { name }) => {
        console.log("Active: " + name)
        this.setState({ activeItem: name }) 
        console.log(this.state.activeItem)
    }

    render() {
        const { activeItem } = this.state
        return (
                <div>
                    <Menu pointing secondary>
                     <Menu.Item header>Dashboard</Menu.Item>
                        <Menu.Item 
                            as={NavLink} 
                            exact to="/" 
                            name="home" 
                            active={activeItem === 'home'} 
                            onClick={this._handleItemClick} 
                        />
                        <Menu.Item 
                            as={NavLink} 
                            to="/devices" 
                            name="devices" 
                            active={activeItem === 'devices'} 
                            onClick={this._handleItemClick} 
                        />
                        <Menu.Item
                            as={NavLink}
                            to="/sensors" 
                            name="sensors" 
                            active={activeItem === 'sensors'} 
                            onClick={this._handleItemClick} 
                        />

                        <Menu.Menu position='right'>
                            <Menu.Item name="logout" active={activeItem === "logout"} onClick={this._handleItemClick} />
                        </Menu.Menu>
                    </Menu>
                </div>
        )
    }
}

export default NavBar;