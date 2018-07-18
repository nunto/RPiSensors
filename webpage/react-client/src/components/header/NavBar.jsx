import React, { Component } from 'react';
import { NavLink } from 'react-router-dom';
import { Menu, Segment } from 'semantic-ui-react';
import CSSTransitionGroup from 'react-transition-group/CSSTransitionGroup';
import Modal from 'react-modal';
import Login from '../style/Login.css'

class NavBar extends Component {
    constructor(props) {
        super(props);
        this.state = {
            activeItem: 'home',
            modalActive: false,
        }
    }
    
    openModal = () => {
        this.setState({ modalActive: true })
    }

    closeModal = () => {
        this.setState({ modalActive: false })
    }

    onOpenModal = () => {
        this.subtitle.style.color = '#4adf6c';
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
                                <Menu.Item name="login" active={activeItem === "logout"} onClick={this.openModal} />
                            </Menu.Menu>
                        </Menu>
                    </div>
                <div>
                    <CSSTransitionGroup transitionName="modalwindow" transitionEnterTimeout={600} transitionLeaveTimeout={600}>
                        <Modal
                            isOpen={this.state.modalActive}
                            onAfterOpen={this.onOpenModal}
                            onRequestClose={this.closeModal}
                            style={styles}
                            contentLabel="Test Modal"
                        >
                            <h2 ref={subtitle => this.subtitle = subtitle}>Login</h2>
                            <div class="container">
                                <label for="uname"><b>Username: </b></label>
                                <input type="text" placeholder="Enter Username" name="uname" required/>
                                
                                <br/>

                                <label for="psw"><b>Password: </b></label>
                                <input type="password" placeholder="Enter Password" name="psw" required/>
                                    
                                <button type="submit" class="submitBtn">Submit</button>
                            </div>
                        </Modal>
                    </CSSTransitionGroup>
                </div>
            </div>
        )
    }
}

const styles = {
    content : {
        top                   : '50%',
        left                  : '50%',
        right                 : 'auto',
        bottom                : 'auto',
        marginRight           : '-50%',
        transform             : 'translate(-50%, -50%)',
        backgroundColor       : '#282c34'
    }
}

export default NavBar;