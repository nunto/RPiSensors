import React, { Component } from 'react';
import { NavLink } from 'react-router-dom';
import { Menu, Segment, Modal, Header, Icon, Button } from 'semantic-ui-react';
import CSSTransitionGroup from 'react-transition-group/CSSTransitionGroup';
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
                <div class="parent">
                    <Modal
                        open={this.state.modalActive}
                        onClose={this.closeModal}
                        style={styles.content}
                        basic
                        closeIcon
                        size='mini'
                    >
                        <Header as='h2'>
                            <Icon name="sign in alternate" style={{color: '#28965A'}} />
                            <Header.Content>Login</Header.Content>
                        </Header>
                        <Modal.Content>
                            <div class="container">
                                <label for="uname"><b>Username: </b></label>
                                <input type="text" placeholder="Enter Username" name="uname" required />
                                
                                <br/>

                                <label for="psw"><b>Password: </b></label>
                                <input type="password" placeholder="Enter Password" name="psw" required />
                            </div>
                        </Modal.Content>
                        <Modal.Actions>
                            <Button style={{backgroundColor: '#28965A'}} animated>
                                <Button.Content visible><h5 class='label-text'>Submit</h5></Button.Content>
                                <Button.Content hidden>
                                    <Icon inverted name='arrow right' />
                                </Button.Content>
                            </Button>
                        </Modal.Actions>
                    </Modal>
                </div>
            </div>
        )
    }
}

const styles = {
    content : {
        position              : 'absolute',
        top                   : '50%',
        left                  : '50%',
        right                 : 'auto',
        bottom                : 'auto',
        marginRight           : '-50%',
        transform             : 'translate(-50%, -50%)',
    }
}

export default NavBar;