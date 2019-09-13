import React from 'react';
import TitleAndLinks from './TitleAndLinks';
import OptionsAndChart from './Options';

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