import React from 'react';
import OptionsForm from './OptionsForm';
import CensusChart from './CensusChart';

import { INDEPENDENT_VAR_OPTION_ID, DEPENDENT_VAR_OPTION_ID, INDEPENDENT_VAR_NAME, DEPENDENT_VAR_NAME } from './Constants';

/**
 * Component containing the variable option form and the census data graph
 */
class OptionsAndChart extends React.Component {
	constructor(props) {
		super(props);
		this.handleFormChange = this.handleFormChange.bind(this);
		this.handleFormSubmit = this.handleFormSubmit.bind(this);
		this.state = {
			independentVar: "EMP",
			dependentVar: "PAYPEREMP",
			censusData: null,
		};
	}
	
	/**
	 * Updates the state of the census variables whenever the option forms are changed
	 * @param {*} event the option that triggered the change event
	 */
	handleFormChange(event) {
		if (event.target.id === INDEPENDENT_VAR_OPTION_ID) {
			this.setState({
				independentVar: event.target.value,
			});
		} else if (event.target.id === DEPENDENT_VAR_OPTION_ID) {
			this.setState({
				dependentVar: event.target.value,
			});
		} else {
			console.log("The options in the HTML select elements did not generate this event.");
		}
	}

	/**
	 * Updates the state of the census data whenever the submit button is clicked by
	 * querying the U.S. Census API
	 * @param {} event 
	 */
	handleFormSubmit(event) {
		if (this.state.independentVar && this.state.dependentVar) {
			// Submit the chosen variables to endpoint, then get the census data response
			const axios = require("axios");
			const dataToPost = {
				[INDEPENDENT_VAR_NAME]: this.state.independentVar,
				[DEPENDENT_VAR_NAME]: this.state.dependentVar,
			};

			// Local host URL used for testing only
			axios.post("http://127.0.0.1:5000/flask-endpoint", dataToPost)
				.then(function (response) {
					return response.data;
				})
				// Need to use arrow function to get the correct reference to 'this'
				.then(data => this.setState({
					censusData: data,
				}))
				.catch(function (error) {
					console.log(error);
				});
		} else if (!this.state.independentVar) {
			console.log("Independent variable not set");
		} else if (!this.state.dependentVar) {
			console.log("Dependent variable not set");
		} else {
			console.log("Case not covered");
		}
	}

	render() {
		return (
			<div>
				<OptionsForm
					onFormChange={this.handleFormChange}
					onFormSubmit={this.handleFormSubmit}
					independentVar={this.state.independentVar}
					dependentVar={this.state.dependentVar}
				/>
				<CensusChart
					independentVar={this.state.independentVar}
					dependentVar={this.state.dependentVar}
					censusData={this.state.censusData}
				/>
			</div>
		);
	}
	
}

export default OptionsAndChart
