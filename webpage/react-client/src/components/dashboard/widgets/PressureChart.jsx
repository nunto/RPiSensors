import React, {Component} from 'react';
import { Chart } from 'react-google-charts';


class PressureChart extends Component {
    constructor() {
        super();
        this.state = {
            sql: {
                query: "SELECT Timestamp, Pressure FROM SensorReadings.dbo.MachineSensorData WHERE SensorID LIKE 'Pressure Sensor'"
            },
             options: {
                title: 'Time vs Pressure',
                hAxis: {title: 'Time'},
                vAxis: {title: 'Pressure'},
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
                    label: 'Pressure'
                }
            ],
        }
    }

    async componentDidMount() {
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
                    graph_id="PressureLineChart"
                    width='100%'
                    legend_toggle 
                />
            </div>
        )
    }


}

export default PressureChart;