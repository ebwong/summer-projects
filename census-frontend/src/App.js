import React from 'react';
import TitleAndLinks from './TitleAndLinks';
import Options from './Options';

class App extends React.Component {
	render() {
		return (
			<div>
			<TitleAndLinks />
			<Options />
			</div>
		);
	}
}

export default App