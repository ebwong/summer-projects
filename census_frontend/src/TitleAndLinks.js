import React from 'react';

/**
 * Title and links to the data sets
 */
class TitleAndLinks extends React.Component {
	render() {
		return (
			<div>
				<h1 id="title"> 2014 SBO and 2012 ASE data visualization</h1>
				<p id="data-sets">
					The 2014 data can be found <a href="https://www.census.gov/data/developers/data-sets/ase.html" rel="noopener noreferrer" target="_blank">here</a> <br />
					The 2012 data can be found <a href="https://www.census.gov/data/developers/data-sets/business-owners.html" rel="noopener noreferrer" target="_blank"> here</a>
				</p>
			</div>


		);
	}
}

export default TitleAndLinks