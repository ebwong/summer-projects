import React from 'react';
import Intro from './Intro';
import DataSelection from './DataSelection';

class App extends React.Component {
	render() {
		return (
			<div>
			<Intro />
			<DataSelection />
			</div>
		);
	}
}

export default App