import React from 'react';

/**
 * A drop-down for users to choose the variable they want to graph
 */
class OptionsForm extends React.Component {

	constructor(props) {
		super(props);
		this.state = { value: "PAYANN" };

		this.handleChange = this.handleChange.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
	}

	handleChange(event) {
		this.setState({value: event.target.value});
	}

	handleSubmit(event) {
		alert("The variable you chose to graph was " + this.state.value);
		event.preventDefault();
		// Call the Flask endpoint
		const data = {
			name: this.state.value,
		};
		const axios = require("axios");
		// axios.defaults.headers.post["Access-Control-Allow-Origin"] = "*";
		axios.post("http://127.0.0.1:5000/post", data)
		.then(function(response) {
			console.log(response)
		})
		.catch(function(error) {
			console.log(error)
		});
	}

	render() {
		return (
			<form id="option-form" onSubmit={this.handleSubmit}>
				<label>Select a variable to graph:
				<select value={this.state.value} onChange={this.handleChange}>
						<option value="PAYANN"> Annual payroll</option>
						<option value="PAYPEREMP"> Average payroll</option>
					</select>
				</label>
				<input type="submit" value="Submit"/>
			</form>
		);
	}
}

export default OptionsForm