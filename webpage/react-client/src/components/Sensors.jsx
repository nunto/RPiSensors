import React, { Component } from 'react';
import { Chart } from 'react-google-charts';

class Sensors extends Component {
    constructor(props) {
        super(props)
        this.state = {
            options: {
                title: 'Time vs Temperature',
                hAxis: {title: 'Time'},
                vAxis: {title: 'Temperature'},
                legend: 'none'
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
            ]
        }
    }
    
    async componentDidMount() {
        await fetch('http://172.18.19.130:8081/retrieve_data.php')
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
                <p>Response: {this.state.rows} ---- {this.state.data}</p>
                <Chart
                    chartType="LineChart"
                    rows={this.state.data}
                    columns={this.state.columns}
                    options={this.state.options}
                    graph_id="LineChart"
                    width="1000px"
                    height="400px"
                    legend_toggle
                />   
            </div>
        )
    }
}

export default Sensors;
