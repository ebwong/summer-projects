import React from 'react';

/**
 * Title and links to the data sets
 */
class TitleAndLinks extends React.Component {
	render() {
		return (
			<div>
				<h1 id="main-page-title"> 2014 U.S. Census SBO Data Visualization</h1>
				<p id="data-sets">
					The 2014 data can be found
					<a
						id="data-2014"
						href="https://www.census.gov/data/developers/data-sets/ase.html"
						rel="noopener noreferrer"
						target="_blank"
					> here</a>
				</p>
			</div>
		);
	}
}

export default TitleAndLinks