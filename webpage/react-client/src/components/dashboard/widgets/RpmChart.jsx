import React, {Component} from 'react';
import { Chart } from 'react-google-charts';


class RpmChart extends Component {
    constructor() {
        super();
        this.state = {
            sql: {
                query: "SELECT Timestamp, RPM FROM SensorReadings.dbo.MachineSensorData WHERE SensorID LIKE 'RPM Sensor' AND RPM < 1000000"
            },
             options: {
                title: 'Time vs RPM',
                hAxis: {title: 'Time'},
                vAxis: {title: 'RPM'},
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
                    label: 'RPM'
                }
            ],
        }
    }

    async componentDidMount() {
        console.log('boutta fetch')
        await fetch('http://172.18.19.102:8081/query.php', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(this.state.sql)
        })
        .then((response) => response.json())
        .then((responseJson) => {
            console.log(responseJson)
            var rows = JSON.parse(responseJson)
            this.setState({ data: rows })
        });
    }

    render() {
        return (
            <div>
                <Chart
                    chartType="LineChart"
                    rows={this.state.data}
                    columns={this.state.columns}
                    options={this.state.options}
                    graph_id="RPMLineChart"
                    width='100%'
                    legend_toggle 
                />
            </div>
        )
    }


}

export default RpmChart;