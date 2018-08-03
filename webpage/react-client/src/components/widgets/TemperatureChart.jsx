import React, { Component } from 'react';
import { Line } from 'react-chartjs-2';

class TemperatureChart extends Component {
    constructor() {
        super();
        this.state = {
            sql: {
                query: "SELECT TOP(50) Timestamp, Temperature FROM SensorReadings.dbo.MachineSensorData WHERE SensorID LIKE 'ThermalProbe'"
            },
            labels: [],
            values: [],
        }
    }

    async componentDidMount() {
        console.log("fetching")
        await fetch('http://172.18.19.130:8081/query.php', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(this.state.sql)
        })
        .then((res) => res.json())
        .then((resJson) => {
            var labels = []
            var values = []
            var data = JSON.parse(resJson)
            for (var i = 0; i < data.length; i++) {
                labels.push(data[i][0]/100000000)
                //console.log("LABEL: " + resJson[i][0])
                values.push(data[i][1])
                //console.log("VALUE: " + resJson[i][1])
            }
            this.setState({ 
                labels: labels,
                values: values
              })
        })

    }

    render() {
        console.log("creating data")
        const data = {
            labels: this.state.labels,
            datasets: [{
                label: 'Temperature',
                fill: 'origin',
                lineTension: 0.2,
                backgroundColor: 'rgba(75,192,192,0.4)',
                borderColor: 'rgba(75,192,192,1)',
                borderCapStyle: 'butt',
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                pointBorderColor: 'rgba(255, 255, 255, 1)',
                pointBackgroundColor: '#fff',
                pointBorderWidth: 1,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: 'rgba(75,192,192,1)',
                pointHoverBorderColor: 'rgba(220,220,220,1)',
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 10,
                data: this.state.values,
            }]
        }
        console.log(data)
        return (
            <div>
                <Line 
                    data={data} 
                    width={350} 
                    height={350} 
                    options={{
                        maintainAspectRatio: false, 
                        animationEasing: 'easeInOutSine', 
                        responsive: true, 
                        animationSteps: 300 
                    }} 
                />
            </div>
        )
    }

}

export default TemperatureChart;