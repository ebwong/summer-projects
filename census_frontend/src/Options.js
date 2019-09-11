import React from 'react';
import DataFrame from 'dataframe-js';
import {VictoryChart, VictoryAxis} from 'victory';

/**
 * A drop-down for users to choose the variable they want to graph
 */
class OptionsForm extends React.Component {

	constructor(props) {
		super(props);
		this.state = {value: "PAYANN"};

		this.handleChange = this.handleChange.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
	}

	handleChange(event) {
		this.setState({value: event.target.value});
	}

	handleSubmit(event) {
		event.preventDefault();
		/*
		const dataToSend = {
			chosenVar: this.state.value,
		};
		// Load axios
		const axios = require("axios");
		axios.post("http://127.0.0.1:5000/flask-endpoint", dataToSend)
		.then(function(response) {
			const columnHeaders = Object.keys(response.data);
			// The data for the DataFrame
			let data = {};
			// Each item in the following list represents a column header and its data
			const categories = Object.values(response.data); 
			// Assign each column of data to the appropriate header/key
			for (let i = 0; i < categories.length; i++) {
				data[columnHeaders[i]] = Object.values(categories[i]);
			}
		
			// Convert the Python DataFrame to a JavaScript DataFrame
			const df = new DataFrame(data, columnHeaders);

			// Iterate over all rows
			for (let i = 0; i < df.count(); i++) {
				const row = df.getRow(i);
				console.log(row);
				let rowVals = [];
				for (let j = 0; j < row.size(); j++) {
					rowVals.push(row.get(columnHeaders[j]))
				}
				console.log(rowVals)
			}

			
		})
		.catch(function(error) {
			console.log(error);
		});
		*/
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
				<CensusChart />
			</form>
		);
	}
}


class CensusChart extends React.Component {
	render() {
		return (
			<div>
				<h1>Census Data</h1>
			</div>

		);
	}
}


class OptionsAndChart extends React.Component {
	render () {
		return (
			<div>
				
			</div>
		)
	}
}

export default OptionsForm