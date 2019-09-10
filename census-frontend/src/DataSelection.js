import React from 'react';

class DataSelection extends React.Component {
	render() {
		return (
			<div id="view-data" onClick={getCensusData}>
			<button>View census data</button>			
			</div>

		);
	}
}

function getCensusData() {
	console.log("You clicked a button")
	const axios = require('axios')
	axios.get("http://127.0.0.1:5000/")
	.then(function (response) {
		console.log(response);
	})
	.catch(function (error) {
		console.log(error)
	})

}

export default DataSelection