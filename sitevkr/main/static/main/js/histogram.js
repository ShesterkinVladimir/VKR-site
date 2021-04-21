
 Highcharts.chart('container', {
  chart: {
    type: 'column'
  },
  title: {
    text: 'data'
  },

  xAxis: {
    type: 'category',
    labels: {
      rotation: 0,
      style: {
        fontSize: '13px',
        fontFamily: 'Verdana, sans-serif'
      }
    },
    title: {
      text: 'Population (millions)'
    }
  },
  yAxis: {
    min: 0,
    title: {
      text: 'Population (millions)'
    }
  },
  legend: {
    enabled: false
  },
  tooltip: {
    pointFormat: 'Population in 2017: <b>{point.y:.1f} millions</b>'
  },
  series: [{
    name: 'Population',
    data: [
      [1, 24.2],
      [2, 20.8],
      [3, 14.9],
      [4, 13.7],
      [5, 13.1],
      [6, 12.7],
      [7, 12.4],
      [8, 12.2],
      [9, 12.0],
      [10, 11.7],
      [11, 11.5],
      [12, 22.2],
      [13, 11.1],
      [14, 30.6],
      [15, 30.6],
      [16, 10.6],
      [17, 10.3],
      [18, 20.8],
      [19, 10.3],
      [20, 9.3]
    ],
    dataLabels: {
      enabled: true,
      rotation: -90,
      color: '#FFFFFF',
      align: 'right',
      format: '{point.y:.1f}', // one decimal
      y: 10, // 10 pixels down from the top
      style: {
        fontSize: '13px',
        fontFamily: 'Verdana, sans-serif'
      }
    }
  }],
  exporting: {
//        showTable: true
        enabled: false
    },
    plotOptions: {
    series: {
        pointPadding: 0, // Defaults to 0.1
        groupPadding: 0, // Defaults to 0.2
        borderWidth: 1,
        color: '#e87464',

    }
},

});



