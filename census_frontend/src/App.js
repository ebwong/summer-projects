import React from 'react';
import TitleAndLinks from './TitleAndLinks';
import OptionsAndChart from './OptionsAndChart';

/**
 * Container React Component that renders all of the information on the
 * webpage
 */
class App extends React.Component {
	render() {
		return (
			<div>
			<TitleAndLinks />
			<OptionsAndChart />
			</div>
		);
	}
}

export default App