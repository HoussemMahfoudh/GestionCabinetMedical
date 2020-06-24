var chart;
		var legend;

		var chartData = [{
				country: "Jquery",
				value: 200
			},
			{
				country: "HTML5",
				value: 340
			},
			{
				country: "Photoshop",
				value: 230
			},
			{
				country: "PHP",
				value: 250
			},
			{
				country: "Bootstrap",
				value: 150
			},
			{
				country: "CSS3",
				value: 200
			}
		];

		AmCharts.ready(function () {
			// PIE CHART
			chart = new AmCharts.AmPieChart();
			chart.dataProvider = chartData;
			chart.titleField = "country";
			chart.valueField = "value";
			chart.outlineColor = "";
			chart.outlineAlpha = 0.8;
			chart.outlineThickness = 2;
			// this makes the chart 3D
			chart.depth3D = 20;
			chart.angle = 30;

			// WRITE
			chart.write("chartdiv");
		});