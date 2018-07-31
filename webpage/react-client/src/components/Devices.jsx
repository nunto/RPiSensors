import React, { Component } from 'react';
import { Grid, Segment, Header, Card, Button, Icon, Modal, Form } from 'semantic-ui-react';
import Login from './style/Login.css'

class Devices extends Component {
    constructor(props) {
        super(props);
        this.state = {
            width: 0,
            height: 0,
            columns: 3,
            modalActive: false,
            editModal: false,
            name: '',
            desc: '',
            submittedName: '',
            submittedDesc: '',
            ctx: 0,
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
                            <Button basic color='green' onClick={this.openEdit} id={0}>Edit</Button>
                        </Button.Group>
                },
                {
                    id: 1,
                    header: 'Pi-2',
                    description: 'Raspberry Pi connected to air compressor 2',
                    meta: 'Active',
                    extra: <Button.Group fluid>
                            <Button basic color='red' onClick={this.removeDevice} id={1}>Remove</Button>
                            <Button basic color='green' onClick={this.openEdit} id={1}>Edit</Button>
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
                            <Button basic color='green' onClick={this.openEdit} id={2}>Edit</Button>
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
                            <Button basic color='green' onClick={this.openEdit} id={3}>Edit</Button>
                        </Button.Group>
                            
                }
            ]
        }
        this.updateWindowDimensions = this.updateWindowDimensions.bind(this);
    }

    componentDidMount() {
        this.updateWindowDimensions();
        window.addEventListener('resize', this.updateWindowDimensions);
    }

    componentWillUnmount() {
        window.removeEventListener('resize', this.updateWindowDimensions);
    }

    updateWindowDimensions() {
        var cols = this.state.columns
        this.setState({ width: window.innerWidth, height: window.innerHeight })
        if (cols === 3) {
            if (window.innerWidth < 450) {
                this.setState({ columns: 1 })
            }
            else if (window.innerWidth < 675) {
                this.setState({ columns: 2})
            }
        }
        else if (cols === 2) {
            if (window.innerWidth < 450) {
                this.setState({ columns: 1 })
            }
            else if (window.innerWidth > 675) {
                this.setState({ columns: 3 })
            }
        }

        else if (cols === 1) {
            if (window.innerWidth > 675) {
                this.setState({ columns: 3 })
            }
            else if (window.innerWidth > 450) {
                this.setState({ columns: 2 })
            }
        }
        console.log("width: " + window.innerWidth + "\nheight: " + window.innerHeight)
    }

    // Opens the edit device modal
    openEdit = (e, data) => {
        this.setState({ 
            ctx: data.id,
            editModal: true 
            })
    }

    // Closes the edit device modal
    closeEdit = () => {
        this.setState({ 
            name: '',
            desc: '',
            editModal: false,
         })
    }

    // Opens the new device modal
    openModal = () => {
        this.setState({ modalActive: true })
    }

    // Closes the new device modal
    closeModal = () => {
        this.setState({ 
            name: '',
            desc: '',
            modalActive: false
        })
    }

    // Removes a device from the list
    removeDevice = (e, data) => {
        var arr = [...this.state.devices];
        var obj = arr.find(device => device.id === data.id)
        arr.splice(arr.indexOf(obj), 1)
        this.setState({ devices: arr })
    }

    // Edit the data of an already defined device
    editDevice = () => {
        var arr = [...this.state.devices];
        var obj = arr.find(device => device.id === this.state.ctx)
        var index = arr.indexOf(obj)
        if (this.state.submittedName.replace(/\s/g, '') !== '') {
            arr[index].header = this.state.submittedName;
        }

        if (this.state.submittedDesc.replace(/\s/g, '') !== '') {
            arr[index].description = this.state.submittedDesc;
        }

        this.setState({ devices: arr })
    }

    // Create a new device
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
                        <Button basic color='green' onClick={this.openEdit} id={index}>Edit</Button>
                    </Button.Group>
        }
        this.setState({ devices: [...this.state.devices, deviceObj] })
    }

    // Handles an input field change
    handleFormChange = (e, { name, value }) => {
        this.setState({ [name]: value })
    }

    // On modal save
    handleEditSave = () => {
        const { name, desc } = this.state

        this.setState({ submittedName: name, submittedDesc: desc }, () => {
            this.setState({ name: '', desc: '' })
            this.closeEdit()
            this.editDevice()
        })
    }

    // On modal submit
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
                                            <Card.Group items={this.state.devices} itemsPerRow={this.state.columns}>
                                                
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
                    
                    <div class="parent">
                        <Modal
                            open={this.state.editModal}
                            onClose={this.closeEdit}
                            style={styles.content}
                            basic
                            closeIcon
                            size='mini'
                        >
                            <Header as='h2'>
                                <Icon name="edit" style={{color: '#28965A'}} />
                                <Header.Content>Edit Device</Header.Content>
                            </Header>
                            <Modal.Content>
                                <Form>
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
                                <Button style={{backgroundColor: '#28965A'}} animated onClick={this.handleEditSave}>
                                    <Button.Content visible><h4 class='label-text'>Save Changes</h4></Button.Content>
                                    <Button.Content hidden>
                                        <Icon inverted name='save alternate' />
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