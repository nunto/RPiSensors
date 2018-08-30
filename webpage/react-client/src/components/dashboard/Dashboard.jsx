import React, { Component } from 'react';
import Dashboard, { addWidget } from 'react-dazzle';

// Dashboard components
import AddWidgetDialog from './AddWidgetDialog';
import Container from './Container';
import CustomFrame from './CustomFrame';
import EditBar from './EditBar';

// Widgets
import TemperatureChart from './widgets/TemperatureChart';
import HumidityChart from './widgets/HumidityChart';
import RpmChart from './widgets/RpmChart';
import AmperageChart from './widgets/AmperageChart';
import FlowChart from './widgets/FlowChart';
import PressureChart from './widgets/PressureChart';

// Styling
import 'bootstrap/dist/css/bootstrap.css';
import 'react-dazzle/lib/style/style.css';
import '../style/custom.css';


class Dash extends Component {
    constructor(props) {
        super(props);
        this.state = {
            widgets: {
                //Widgets should go here
                TemperatureWidget: {
                    type: TemperatureChart,
                    title: 'Temperature'
                },
                HumidityWidget: {
                    type: HumidityChart,
                    title: 'Humidity'
                },
                RPMWidget: {
                    type: RpmChart,
                    title: 'RPM',
                },
                AmpWidget: {
                    type: AmperageChart,
                    title: 'Amperage'
                },
                FlowWidget: {
                    type: FlowChart,
                    title: 'Flow'
                },
                PressureWidget: {
                    type: PressureChart,
                    title: 'Pressure'
                }
            },
            layout: {
                rows: [{
                    columns: [{
                        className: 'col-md-12 col-sm-12 col-xs-12',
                        widgets: [{key: 'AmpWidget'}],
                    }],
                }, {
                    columns: [{
                        className: 'col-md-6 col-sm-6 col-xs-6',
                        widgets: [{key: 'TemperatureWidget'}, {key: 'HumidityWidget'}],
                    }, {
                        className: 'col-md-6 col-sm-6 col-xs-6',
                        widgets: [{key: 'RPMWidget'}, {key: 'PressureWidget'}],
                    }],
                }],
            },
            editing: false,
            isModalOpen: false,
            addWidgetOptions: null,
        };
    }

    onRemove = (layout) => {
        this.setState({ layout: layout });
    }

    onAdd = (layout, rowIndex, columnIndex) => {
        this.setState({ 
            isModalOpen: true,
            addWidgetOptions: {
                layout,
                rowIndex,
                columnIndex
            }
        });
    }

    onMove = (layout) => {
        this.setState({ layout: layout });
    }

    onRequestClose = () => {
        this.setState({ isModalOpen: false });
    }

    toggleEdit = () => {
        this.setState({ editMode: !this.state.editMode });
    }

    handleWidgetSelection = (widgetName) => {
        const {layout, rowIndex, columnIndex} = this.state.addWidgetOptions;

        this.setState({ layout: addWidget(layout, rowIndex, columnIndex, widgetName) })

        this.onRequestClose();
    }

    render() {
        return (
            <Container>
                <AddWidgetDialog widgets={this.state.widgets} isModalOpen={this.state.isModalOpen} onRequestClose={this.onRequestClose} onWidgetSelect={this.handleWidgetSelection}/>
                <EditBar onEdit={this.toggleEdit} />
                <Dashboard
                    frameComponent={CustomFrame}
                    onRemove={this.onRemove}
                    layout={this.state.layout}
                    widgets={this.state.widgets}
                    editable={this.state.editMode}
                    onAdd={this.onAdd}
                    onMove={this.onMove}
                    addWidgetComponentText="Add New Widget"
                />
            </Container>
        );
    }
}

export default Dash;