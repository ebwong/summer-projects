import React from 'react';
import DataFrame from 'dataframe-js';
import { VictoryChart, VictoryAxis, VictoryScatter, VictoryLegend} from 'victory';

/**
 * The graph of the census data
 * @param {*} props 
 */
function CensusChart(props) {
	// For formatting point colors
	const HEX_COLOR_PREFIX = "#";
	const COLORS = [
		"FF0000", // Red
		"FFA500", // Orange
		"FFFF00", // Yellow
		"008000", // Green
		"0000FF", // Blue
		"4B0082", //vindigo
		"EE82EE", //violet
		"00FFFF", //cyan
		"FF00FF", //magenta
		"FFD700", //gold
		"00BFFF", //deep sky blue
		"000080", //navy
		"FF1493", //deep pink
		"FFC0CB", //pink
		"8B4513", //saddle brown
		"D2691E", //chocolate
		"708090", //slate gray
		"800080", //purple
		"00FF00", //lime
		"FA8072", //salmon
		"000000", //black
	]

	let groupCodes = []; // Groups to classify data by
	let groups = [];	

	// These index values are determined by the backend
	const GROUP_INDEX = 0;
	const GROUP_TTL_INDEX = 1;
	const X_VAR_INDEX = 2;
	const Y_VAR_INDEX = 3;

	const TICK_SCALER = 1000;

	const xVar = props.independentVar;
	const yVar = props.dependentVar;
	let xVals = [];
	let yVals = [];

	let pointsToPlot = [];

	if (props.censusData) {
		const columnHeaders = Object.keys(props.censusData);

		// The data for the DataFrame
		let dataForDF = {};

		// Each item in the array below represents a column header key and its data value
		const categories = Object.values(props.censusData);

		// Assign each column of data to the appropriate header/key
		for (let i = 0; i < categories.length; i++) {
			dataForDF[columnHeaders[i]] = Object.values(categories[i]);
		}

		// Get the JavaScript DataFrame equivalent
		const df = new DataFrame(dataForDF, columnHeaders);

		// Get the data needed for each point from each row
		for (let i = 0; i < df.count(); i++) {
			const row = df.getRow(i).toArray();
			groupCodes.push(row[GROUP_INDEX]);
			groups.push(row[GROUP_TTL_INDEX]);
			xVals.push(row[X_VAR_INDEX]);
			yVals.push(row[Y_VAR_INDEX]);

			// Add a point to be plotted
			const point = {
				x: row[X_VAR_INDEX],
				y: row[Y_VAR_INDEX],
				label: row[GROUP_INDEX],
				fill: HEX_COLOR_PREFIX + COLORS[i],
			};
			pointsToPlot.push(point);
		}
		
		// Legend formatting
		let legendData = [];
		for (let i = 0; i < groupCodes.length; i++) {
			legendData.push({
				name: groupCodes[i] + " = " + groups[i],
			});
		}

		return (
			<div>
				<h1 id="chart-title">{yVar + " vs " + xVar}</h1>
				<VictoryChart
					animate={{
						duration: 2000,
						easing: "bounce",
					}}
					domainPadding={10}
				
					height={1000}
					width={1500}
					padding={{top: 50, bottom: 75, left: 75, right: 75}}
				>
					<VictoryAxis
						label={xVar}
						fixLabelOverlap
						style={{
							axisLabel: {fontSize: 16, padding: 30},
							tickLabels: {fontSize: 14, padding: 0},
						}}
					/>
					<VictoryAxis
						dependentAxis
						label={yVar}
						fixLabelOverlap

						style={{
							axisLabel: {fontSize: 16, padding: 60},
							tickLabels: {fontSize: 14, padding: 30},

						}}
					/>

					<VictoryScatter
					size={3}
					data = {pointsToPlot}
					scale = {{x: "linear", y: "linear"}}
					style={{
						data: {
							fill: ({datum}) => datum.fill,
						},
						labels: {fontSize: 12}
					}}
					/>
					<VictoryLegend 
					title="Legend"
					centerTitle
					colorScale={COLORS}
					data={legendData}
					orientation="vertical"
					style={{
						border: {stroke: "black"},						
					}}
					x={1000}
					y={300}					
					/>
				</VictoryChart>
			</div>
		);
	} else {
		return (
			<div>
			</div>
		);
	}
}

export default CensusChart