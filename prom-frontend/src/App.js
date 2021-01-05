import logo from './logo.svg';
import './App.css';
import Charts from './components/Charts';
import { useEffect, useState } from 'react';
import axios from "axios";
import {Line,Scatter} from "react-chartjs-2";
function App() {

  const [backendData, setBackendData] = useState([]);
  const [chartData, setChartData] = useState([{}]);
  const [optionData, setOptionData] = useState([{}]);
  const [zscoredata1, setzscoredata1] = useState([]);
  const [zscoredata2, setzscoredata2] = useState([]);
  const [sentence, setSentence] = useState([])
  const [sentence1, setSentence1] = useState("");
  const [sentence2, setSentence2] = useState("");

  const chart = () => {
    axios.get("http://127.0.0.1:5000/a/wine")
    .then(res => {
      // console.log(res.data)

      // what needs to happen?
      // first, create a chart with random points and have it display
      // data = JSON.parse(res.data);

      let d = JSON.stringify(res.data)
      d = JSON.parse(d);

      // console.log(res.data.zscore);

      let zs = JSON.stringify(res.data.zscore)
      zs = JSON.parse(zs);
      // console.log(zs.zscoredata2);

      setzscoredata1(zs.zscoredata1);
      setzscoredata2(zs.zscoredata2);
      setSentence1(zs.sentence1);
      setSentence2(zs.sentence2);
      // console.log(zs);




      // console.log(d)
      // setBackendData(d)
      let dataArray = []
      let optionArray = []
      let sentenceArray = [];

      // for loop iterating through each item in the list, creating a list of dictionaries that look like the one below
      for(const dataObj of d.data){
      
      let c = {

        labels: ['catter'],
        datasets: [
          {
            label: 'My First dataset',
            fill: false,
            // showLine: true,  //!\\ Add this line
            backgroundColor: 'rgba(75,192,192,0.4)',
            pointBorderColor: 'rgba(75,192,192,1)',
            pointBackgroundColor: "#0099CC",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: 'rgba(75,192,192,1)',
            pointHoverBorderColor: 'rgba(220,220,220,1)',
            pointHoverBorderWidth: 2,
            pointRadius: 5,
            pointHitRadius: 10,
            data: dataObj.coords
            
         
          },
          {
            type: 'line',
            label: 'Line of best fit',
            data: dataObj.line_of_best_fit,
            fill: false,
            backgroundColor: '#71B37C',
            borderColor: '#71B37C',
            hoverBackgroundColor: '#71B37C',
            hoverBorderColor: '#71B37C',
            yAxisID: 'y-axis-1'
          }
        ]

        

      }

      // console.log(c);
      // console.log(dataObj.col2);
      let o = {
        legend: {
          display: false
       },
        scales: {
          xAxes: [{
            display: true,
            scaleLabel: {
              display: true,
              labelString: dataObj.col1
            }
          }],
          yAxes: [{
            display: true,
            scaleLabel: {
              display: true,
              labelString: dataObj.col2
            }
          }]
       
        }     
      }

  


      dataArray.push(c);
      optionArray.push(o);
      
      sentenceArray.push(dataObj.sentence);

    }

    

    setChartData(dataArray);
    setOptionData(optionArray);
    setSentence(sentenceArray)
    


    // console.log(chartData);
    // console.log(optionData);
    







      



     






    })
    .catch(err => {
      console.log(err)
    })
  }
  const data = {
    labels: ['Scatter'],
    datasets: [
      {
        label: 'My First dataset',
        fill: false,
        // showLine: true,  //!\\ Add this line
        backgroundColor: 'rgba(75,192,192,0.4)',
        pointBorderColor: 'rgba(75,192,192,1)',
        pointBackgroundColor: '#fff',
        pointBorderWidth: 1,
        pointHoverRadius: 5,
        pointHoverBackgroundColor: 'rgba(75,192,192,1)',
        pointHoverBorderColor: 'rgba(220,220,220,1)',
        pointHoverBorderWidth: 2,
        pointRadius: 5,
        pointHitRadius: 10,
        data: backendData
        
     
      }
    ]
  };

  const dataa = {
    labels: ['Scatter'],
    datasets: [
      {
        label: 'My First dataset',
        fill: false,
        backgroundColor: 'rgba(75,192,192,0.4)',
        pointBorderColor: 'rgba(75,192,192,1)',
        pointBackgroundColor: '#fff',
        pointBorderWidth: 1,
        pointHoverRadius: 5,
        pointHoverBackgroundColor: 'rgba(75,192,192,1)',
        pointHoverBorderColor: 'rgba(220,220,220,1)',
        pointHoverBorderWidth: 2,
        pointRadius: 10,
        pointHitRadius: 10,
        data: backendData
      }
    ]
  };
  


//   chartData = {
//     datasets:[
//         {
//             label: "S11 Polar Graph",
//             fill: false,
//             backgroundColor: this.props.color,
//             pointBorderColor: this.props.color,
//             pointBackgroundColor: '#ffffff',
//             pointBorderWidth: 1,
//             pointHoverRadius: 5,
//             pointRadius: 3,
//             pointHitRadius: 10,
//             data: backendData
//         }
//     ]
// }

// const chartOptions = {
//   maintainAspectRatio: false,
//   showLine: true,
//   scales: {
//       xAxes: [{
//           display: true,
//           labelString: "Hi"
//       }],
//       yAxes: [{
//           display: true,
//           labelString: "Bye"
//       }]
//   }
// }

//   { x: 65, y: 75 },
//   { x: 59, y: 49 },
//   { x: 80, y: 90 },
//   { x: 81, y: 29 },
//   { x: 56, y: 36 },
//   { x: 55, y: 25 },
//   { x: 40, y: 18 },
// ]


// options={{


//   options: {
//     scales: {
//       yAxes: [{
//           ticks: {
//             beginAtZero: true,
//             stepSize: 0.01 //<-- set this
//           }
//       }],
//       xAxes: [{
//         ticks: {
//           beginAtZero: true,
//           stepSize: 0.01 //<-- set this
//         }
//     }]
//     }
//   }



// }}
  useEffect(() => {
    chart()
  },[])
  return (
    <div className="App">
      {/* {chart()} */}
      {/* <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header> */}
      {/* <div><Scatter data = {chartData} /></div> */}
      <Charts  data ={chartData} option = {optionData} zscoredata1 = {zscoredata1} zscoredata2 = {zscoredata2} sentences = {sentence} sentence1 = {sentence1} sentence2 = {sentence2}/> 
      
    </div>
  );
}

export default App;
