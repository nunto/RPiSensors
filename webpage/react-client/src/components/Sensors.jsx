import React, { Component } from 'react';
import { Chart } from 'react-google-charts';
import { Sidebar, Button, Segment, Menu, Header, Grid } from 'semantic-ui-react';
import SensorStylefrom from './style/SensorStyle.css';

class Sensors extends Component {
    constructor(props) {
        super(props)
        this.state = {
            options: {
                title: 'Time vs Temperature',
                hAxis: {title: 'Time'},
                vAxis: {title: 'Temperature'},
                legend: 'none',
                colors: ['#28965A']
            },
            columns: [
                {
                    type: 'number',
                    label: 'Time'
                },
                {
                    type: 'number',
                    label: 'Temperature'
                }
            ],
            visible: false,
            menuTitle: "Summary",
        }
        this.handleGraphUpdate = this.handleGraphUpdate.bind(this)
    }

    // Called when refresh is clicked
    // Retrieves current data and forces a refresh
    handleGraphUpdate = () => {
        this.dataUpdate()
        .then(() => this.forceUpdate())
    }
    
    // Updates the data via a call to the respective php file
    async dataUpdate() {
        await fetch('http://172.18.19.102:8081/retrieve_data.php')
        .then((response) => response.json())
        .then((responseJson) => {
            console.log(responseJson)
            var rows = JSON.parse(responseJson)
            console.log(rows)
            this.setState({ data: rows })

        })
    }

    // Changes whether sidebar is visible or not
    handleButtonClick = () => this.setState({ visible: !this.state.visible })

    // Hides sidebar
    handleSidebarHide = () => this.setState({ visible: false })

    // Handles a sidebar menu option selection
    handleMenuSelect = (e, {name}) => {
        this.setState({ 
            menuTitle: name,
            visible: false
         })
         this.handleButtonClick()
    }

    // Retrieves initial data
    async componentDidMount() {
        await fetch('http://172.18.19.107:8081/retrieve_data.php')
        .then((response) => response.json())
        .then((responseJson) => {
            console.log(responseJson)
            var rows = JSON.parse(responseJson)
            this.setState({ data: rows })

        })

        console.log(this.state.data)
    }

    render () {
        return (
            <div>
                <div>
                    <Button onClick={this.handleButtonClick} style={{margin: '12px', backgroundColor: '#28965A', color: 'white', display: 'inline-block'}}>
                        Select by...
                    </Button>
                    <Button onClick={this.handleGraphUpdate} style={{margin: '12px', backgroundColor: '#28965A', color: 'white', display: 'inline-block', float:'right'}}>Refresh</Button>
                    <Sidebar.Pushable as={Segment}>
                        <Sidebar
                            as={Menu}
                            animation='scale down'
                            onHide={this.handleSideBarHide}
                            vertical
                            visible={this.state.visible}
                            width='thin'>
                            <Menu.Item as='a' name="Summary" onClick={this.handleMenuSelect}/>
                            <Menu.Item as='a' name="Cost" onClick={this.handleMenuSelect}/>
                        </Sidebar>
                        <Sidebar.Pusher>
                            <Segment basic>
                                <Header as='h3' style={{color: '#28965A'}}>{this.state.menuTitle}</Header>
                                <div>
                                    <Grid columns={2} doubling>
                                        <Grid.Column>
                                            <Segment>
                                                <Chart
                                                    chartType="LineChart"
                                                    rows={this.state.data}
                                                    columns={this.state.columns}
                                                    options={this.state.options}
                                                    graph_id="LineChart"
                                                    width='100%'
                                                    legend_toggle 
                                                />
                                            </Segment>

                                            <Segment>
                                                <Chart
                                                    chartType="AreaChart"
                                                    rows={this.state.data}
                                                    columns={this.state.columns}
                                                    options={this.state.options}
                                                    graph_id="AreaChart"
                                                    width='100%'
                                                    legend_toggle 
                                                />
                                            </Segment>
                                        </Grid.Column>

                                        <Grid.Column>
                                            <Segment>
                                                <Chart
                                                    chartType="ScatterChart"
                                                    rows={this.state.data}
                                                    columns={this.state.columns}
                                                    options={this.state.options}
                                                    graph_id="ScatterChart"
                                                    width='100%'
                                                    legend_toggle 
                                                />
                                            </Segment>

                                            <Segment>
                                                <Chart
                                                    chartType="ColumnChart"
                                                    rows={this.state.data}
                                                    columns={this.state.columns}
                                                    options={this.state.options}
                                                    graph_id="ColumnChar"
                                                    width='100%'
                                                    legend_toggle 
                                                />
                                            </Segment>
                                        </Grid.Column>
                                    </Grid>
                                </div>
                            </Segment>
                        </Sidebar.Pusher>
                    </Sidebar.Pushable>
                </div>
            </div>
        )
    }
}

export default Sensors;
