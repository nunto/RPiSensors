import React, { Component } from 'react';
import { Chart } from 'react-google-charts';

class Sensors extends Component {
    constructor(props) {
        super(props)
        this.state = {
            data: [],
            options: {
                title: 'Time vs Temperature',
                hAxis: {title: 'Time', minValue: 1530818425, maxValue: 1530817930 },
                vAxis: {title: 'Temperature', minValue: 20, maxValue: 30},
                legend: 'none'
            },
        }
    }
    
    async componentDidMount() {
        await fetch('http://172.18.19.130:8081/retrieve_data.php')
        .then((response) => response.json())
        .then((responseJson) => {
            console.log(responseJson)
            this.setState({ data: responseJson })
        })

        console.log(this.state.data)
    }

    render () {
        return (
            <div>
                <p>Response: {this.state.response}</p>
                <Chart
                    chartType="LineChart"
                    data={this.state.data}
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
