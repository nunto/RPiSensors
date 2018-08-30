import React, { Component } from 'react';
import { Button, FormGroup, FormControl, ControlLabel } from 'react-bootstrap';
import "./style/Login.css";

class Login extends Component {
    constructor(props) {
        super(props);
        this.state = {
            email: '',
            password: ''
        }
    }
    
    // Validation, currently only checks for length
    validateForm = ()  => {
        console.log("validating form")
        return this.state.email.length > 0 && this.state.password.length > 0;
    }

    // On Form change
    handleChange = (event) => {
        // The default action of the event will not be triggered
        event.preventDefault();
    }

    hanldeSubmit = async event => {
        alert('Logged in.');
    }

    render() {
        return (
            <div className="Login">
                <form onSubmit={this.handleSubmit}>
                    <FormGroup controlId="email" bsSize="large">
                        <ControlLabel>Email: </ControlLabel>
                        <FormControl
                            autoFocus
                            type="email"
                            defaultValue={this.state.email}
                            onChange={this.handleChange}
                        />
                    </FormGroup>
                    <FormGroup controlId="password" bsSize="large">
                        <ControlLabel>Password: </ControlLabel>
                        <FormControl
                            defaultValue={this.state.password}
                            onChange={this.handleChange}
                            type="password"
                        />
                    </FormGroup>
                    <Button
                        block
                        bsSize="large"
                        disabled={!this.validateForm}
                        type="submit"
                    >
                    Login
                    </Button>
                </form>
            </div>
        );
    }
}

export default Login;