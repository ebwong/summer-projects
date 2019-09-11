import React from 'react';
import ReactDOM from 'react-dom';
import {VictoryBar} from 'victory';
import Main from './VictoryGraph';


class DataSelection extends React.Component {
	render() {
		return (
			<div id="view-data">
				<button>View census data</button>
			</div>

		);
	}
}



function getCensusData() {
	console.log("You clicked the data button")
	const axios = require('axios')
	axios.get("http://127.0.0.1:8000/")
		.then(function (response) {
			console.log(response.data);
		})
		.catch(function (error) {
			console.log(error)
		})

}

export default DataSelection