import React from 'react';
import DataFrame from 'dataframe-js';
import { VictoryChart, VictoryAxis, VictoryScatter } from 'victory';

/**
 * A drop-down for users to choose the variable they want to graph
 */
class OptionsForm extends React.Component {

	constructor(props) {
		super(props);
		this.handleChange = this.handleChange.bind(this);
	}

	handleChange(event) {
		this.props.onFormChange(event.target.value);
	}

	render() {
		return (
			<form id="option-form" onSubmit={this.handleSubmit}>
				<label>Select a variable to graph:
				<select onChange={this.handleChange}>
						<option value="PAYPEREMP"> Annual payroll per employee</option>
					</select>
				</label>
			</form>
		);
	}
}

/**
 * The graph of the census data
 * @param {*} props 
 */
function CensusChart(props) {
	let groups = []; // Groups to classify data by

	const GROUP_INDEX = 0;
	const GROUP_TTL_INDEX = 1;
	const X_VAR_INDEX = 2;
	const Y_VAR_INDEX = 3;
	const TICK_SCALER = 1000;

	let xVar;
	let yVar;
	let xVals = [];
	let yVals = [];

	let pointsToPlot = [];

	if (props.censusData) {
		const columnHeaders = Object.keys(props.censusData);

		// Get the x- and y- variables to be plotted
		xVar = columnHeaders[X_VAR_INDEX];
		yVar = columnHeaders[Y_VAR_INDEX];

		// The data for the DataFrame
		let dataForDF = {};

		// Each item in the array below represents a column header key and its data value
		const categories = Object.values(props.censusData);

		// Assign each column of data to the appropriate header/key
		for (let i = 0; i < categories.length; i++) {
			dataForDF[columnHeaders[i]] = Object.values(categories[i]);
		}

		// Get the JavaScript DataFrame equivalent
		const df = new DataFrame(dataForDF, columnHeaders);

		// Get the relevant data from each row
		for (let i = 0; i < df.count(); i++) {
			const row = df.getRow(i).toArray();
			groups.push(row[GROUP_TTL_INDEX]); // Get GROUP_TTL
			xVals.push(row[X_VAR_INDEX]);
			yVals.push(row[Y_VAR_INDEX]);

			// Add a point to be plotted
			const point = {
				x: row[X_VAR_INDEX],
				y: row[Y_VAR_INDEX],
				label: row[GROUP_INDEX],
			};
			pointsToPlot.push(point);
		}
		
		console.log(pointsToPlot);

		// Format graph

		// Get the min and max to draw the tick values
		// Destructure arrays with "..." to get the min and max values
		// Scale the values for ease of graphing
		let xMinVal = Math.min(...xVals);
		let xMaxVal = Math.max(...xVals);

		let yMinVal = Math.min(...yVals);
		let yMaxVal = Math.max(...yVals);
		// 						tickFormat={(x) => (`${x}k`)}


// 						tickFormat={(y) => (`${y}k`)}

		return (
			<div>
				<h1 id="chart-title">{yVar + " vs " + xVar}</h1>
				<VictoryChart
					domainPadding={10}
					domain={{ 
						x: [xMinVal, xMaxVal], 
						y: [yMinVal, yMaxVal], 
					}}
					height={1000}
					width={1500}
					padding={{top: 50, bottom: 75, left: 75, right: 75}}
				>
					<VictoryAxis
						label={xVar}
						fixLabelOverlap
						style={{
							axisLabel: {fontSize: 16, padding: 30},
							tickLabels: {fontSize: 14, padding: 0},
						}}
					/>
					<VictoryAxis
						dependentAxis
						label={yVar}
						fixLabelOverlap

						style={{
							axisLabel: {fontSize: 16, padding: 60},
							tickLabels: {fontSize: 14, padding: 30},

						}}
					/>

					<VictoryScatter
					size={3}
					data = {pointsToPlot}
					scale = {{x: "linear", y: "linear"}}
					style={{
						labels: {fontSize: 12}
					}}
					/>


				</VictoryChart>

			</div>
		);


	} else {
		return (
			<div>
				<h1 id="loading">LOADING ...</h1>
			</div>
		);
	}

}


class OptionsAndChart extends React.Component {
	constructor(props) {
		super(props);
		this.handleFormChange = this.handleFormChange.bind(this);
		this.state = {
			censusVar: "PAYPEREMP",
			censusData: null,
		};
	}

	handleFormChange(value) {
		const axios = require("axios");

		// Submit the chosen variable to endpoint, then get the census data response
		axios.post("http://127.0.0.1:5000/flask-endpoint", { chosenVar: value })
			.then(function (response) {
				return response.data;
			})
			// Need to use arrow function to get correct 'this'
			.then(data => this.setState({
				censusVar: value,
				censusData: data,

			}))
			.catch(function (error) {
				console.log(error);
			});
	}

	componentDidMount() {
		const axios = require("axios");

		// Submit the chosen variable to endpoint, then get the census data response
		axios.post("http://127.0.0.1:5000/flask-endpoint", { chosenVar: this.state.censusVar })
			.then(function (response) {
				return response.data;
			})
			// Need to use arrow function to get correct 'this'
			.then(data => this.setState({
				censusData: data,
			}))
			.catch(function (error) {
				console.log(error);
			});
	}


	render() {
		// Upon startup, the data won't be ready, so only render the
		// data once the data has been retrieved
		if (this.state.censusData) {
			return (
				<div>
					<OptionsForm
						onFormChange={this.handleFormChange}
						censusVar={this.state.censusVar}
					/>
					<CensusChart
						censusVar={this.state.censusVar}
						censusData={this.state.censusData}
					/>
				</div>
			);

		} else {
			return (
				<div>
					<OptionsForm
						onFormChange={this.handleFormChange}
						censusVar={this.state.censusVar}
					/>
					<CensusChart
						censusVar={this.state.censusVar}
						censusData={this.state.censusData}
					/>
				</div>
			);

		}

	}
}

export default OptionsAndChart
