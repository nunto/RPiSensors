import React, { Component } from 'react';
import { Grid, Segment, Header, Card, Button, Icon, Modal, Form } from 'semantic-ui-react';
import Login from './style/Login.css'

class Devices extends Component {
    constructor(props) {
        super(props);
        this.state = {
            modalActive: false,
            name: '',
            desc: '',
            submittedName: '',
            submittedDesc: '',
            // Devices list is used to dynamically add/remove cards
            // Need a way to id each one.
            devices: [
                {
                    id: 0,
                    header: 'Pi-1',
                    description: 'Raspberry Pi connected to air compressor 1',
                    meta: 'Active',
                    extra: <Button.Group fluid>
                            <Button basic color='red' onClick={this.removeDevice} id={0}>Remove</Button>
                            <Button basic color='green'>Edit</Button>
                        </Button.Group>
                },
                {
                    id: 1,
                    header: 'Pi-2',
                    description: 'Raspberry Pi connected to air compressor 2',
                    meta: 'Active',
                    extra: <Button.Group fluid>
                            <Button basic color='red' onClick={this.removeDevice} id={1}>Remove</Button>
                            <Button basic color='green'>Edit</Button>
                        </Button.Group>
                },
                {
                    id: 2,
                    color: 'olive',
                    header: 'Arduino-1',
                    description: 'Arduino connected to heater',
                    meta: 'Active',
                    extra: <Button.Group fluid>
                            <Button basic color='red' onClick={this.removeDevice} id={2}>Remove</Button>
                            <Button basic color='green'>Edit</Button>
                        </Button.Group>
                            
                },
                {
                    id: 3,
                    color: 'olive',
                    header: 'Arduino-2',
                    description: 'Arduino connected to fan',
                    meta: 'Active',
                    extra: <Button.Group fluid>
                            <Button basic color='red' onClick={this.removeDevice} id={3}>Remove</Button>
                            <Button basic color='green'>Edit</Button>
                        </Button.Group>
                            
                }
            ]
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

    removeDevice = (e, data) => {
        var arr = [...this.state.devices];
        var obj = arr.find(device => device.id === data.id)
        arr.splice(arr.indexOf(obj), 1)
        this.setState({ devices: arr })
    }

    handleNewDevice = () => {
        var index = this.state.devices.length;
        var deviceObj = {
            id: index,
            color: 'olive',
            header: this.state.name,
            description: this.state.desc,
            meta: 'Active',
            extra: <Button.Group fluid>
                        <Button basic color='red' onClick={this.removeDevice} id={index}>Remove</Button>
                        <Button basic color='green'>Edit</Button>
                    </Button.Group>
        }
        this.setState({ devices: [...this.state.devices, deviceObj] })
    }

    handleFormChange = (e, { name, value }) => {
        this.setState({ [name]: value })
    }

    handleSubmit = () => {
        const { name, desc } = this.state
        
        this.setState({ submittedName: name, submittedDesc: desc }, () => {
            this.setState({ name: '', desc: '' })
            this.closeModal()
            this.handleNewDevice()
        })
        
    }

    render () {
        const { name, desc } = this.state
        
        if(this.state.devices.length !== 0) {
            return (
                <div>
                    <div>
                        <Button style={{margin: '12px', backgroundColor: '#28965A', color: 'white', display: 'inline-block'}} animated onClick={this.openModal}>
                            <Button.Content visible><h4 class='label-text'>New Device</h4></Button.Content>
                            <Button.Content hidden>
                                <Icon inverted name='plus circle' />
                            </Button.Content>
                        </Button>
                        <Segment basic>
                            <div>
                                <Grid columns={1} doubling>
                                    <Grid.Column>
                                        <Segment>
                                            <Header as='h3' style={{color: '#28965A'}}>
                                                Your Devices
                                            </Header>
                                            <Card.Group items={this.state.devices} itemsPerRow={3}>
                                                
                                            </Card.Group>
                                        </Segment>
                                    </Grid.Column>
                                </Grid>
                            </div>
                        </Segment>
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
                                <Form onSubmit={this.handleSubmit}>
                                    <Form.Input
                                        placeholder='Name'
                                        name='name'
                                        value={name}
                                        onChange={this.handleFormChange}
                                    />
                                    <Form.Input
                                        placeholder='Description'
                                        name='desc'
                                        value={desc}
                                        onChange={this.handleFormChange}
                                    />
                                </Form>
                            </Modal.Content>
                            <Modal.Actions>
                                <Button style={{backgroundColor: '#28965A'}} animated onClick={this.handleSubmit}>
                                    <Button.Content visible><h4 class='label-text'>Submit</h4></Button.Content>
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
        else {
            return (
                <div>
                    <Button style={{margin: '12px', backgroundColor: '#28965A', color: 'white', display: 'inline-block'}} animated onClick={this.openModal}>
                            <Button.Content visible><h4 class='label-text'>New Device</h4></Button.Content>
                            <Button.Content hidden>
                                <Icon inverted name='plus circle' />
                            </Button.Content>
                        </Button>
                    You have no devices; select <b>new device</b> to get started
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
                                <Form onSubmit={this.handleSubmit}>
                                    <Form.Input
                                        placeholder='Name'
                                        name='name'
                                        value={name}
                                        onChange={this.handleFormChange}
                                    />
                                    <Form.Input
                                        placeholder='Description'
                                        name='desc'
                                        value={desc}
                                        onChange={this.handleFormChange}
                                    />
                                </Form>
                            </Modal.Content>
                            <Modal.Actions>
                                <Button style={{backgroundColor: '#28965A'}} animated onClick={this.handleSubmit}>
                                    <Button.Content visible><h4 class='label-text'>Submit</h4></Button.Content>
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

export default Devices;
