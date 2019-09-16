import React from 'react';
import {INDEPENDENT_VAR_OPTION_ID, DEPENDENT_VAR_OPTION_ID} from './Constants';

/**
 * A drop-down for users to choose the variable they want to graph
 */
class OptionsForm extends React.Component {

	constructor(props) {
		super(props);
		this.handleChange = this.handleChange.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
	}

	handleChange(event) {
		this.props.onFormChange(event);
	}

	handleSubmit(event) {
		event.preventDefault();
		this.props.onFormSubmit(event);
	}

	render() {
		return (
			<form id="option-form" onSubmit={this.handleSubmit}>
				<label className="var-label">Select a variable to graph on the x-axis:
				<select id={INDEPENDENT_VAR_OPTION_ID} defaultValue="EMP" onChange={this.handleChange}>
						<option className="var-option" value="EMP">Number of employees</option>
					</select>
				</label>
				<br />
				<label className="var-label"> Select a variable to graph on the y-axis:
				<select id={DEPENDENT_VAR_OPTION_ID} defaultValue="PAYPEREMP" onChange = {this.handleChange}>
					<option className="var-option" value="PAYPEREMP">Annual payroll per employee</option>
					<option className="var-option" value="EMPPERFIRM">Number of employees per firm</option>
					</select>
				</label>
				<br />
				<input id="submit-vars" type="submit" value="Graph!"/>
			</form>
		);
	}
}

export default OptionsForm