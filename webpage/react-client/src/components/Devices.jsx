import React, { Component } from 'react';
import { Grid, Segment, Header, Card, Button } from 'semantic-ui-react';

class Devices extends Component {
    render () {
        return (
            <div>
                <Segment basic>
                    <Header as='h3' style={{color: '#28965A'}}>Your Devices</Header>
                    <div>
                        <Grid columns={1} doubling>
                            <Grid.column>
                                <Segment>
                                    <Card.Group>
                                        <Card>
                                            <Card.Content>
                                                <Card.Header>Pi-1</Card.Header>
                                                <Card.Meta>Active</Card.Meta>
                                                <Card.Description>
                                                    Raspberry Pi connected to air compressor 1
                                                </Card.Description>
                                            </Card.Content>
                                            <Card.Content extra>
                                                <div className='ui two buttons'>
                                                    <Button basic color='green'>
                                                        Edit
                                                    </Button>
                                                    <Button basic color='red'>
                                                        Remove
                                                    </Button>
                                                </div>
                                            </Card.Content>
                                        </Card>
                                    </Card.Group>
                                </Segment>
                            </Grid.column>
                        </Grid>
                    </div>
                </Segment>
            </div>
        )
    }
}

export default Devices;
