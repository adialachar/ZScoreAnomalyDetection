import React, {Component} from 'react';
import {Bar, Scatter} from 'react-chartjs-2';
import './Charts.css';

class Charts extends Component{
    render(){
        
        console.log("YOOOOO");
        console.log(this.props.zscoredata1);
        var things = []

        var bars = [];
        var chart1Labels = [];
        var chart1data = [];
        var chart2Labels = [];
        var chart2data = [];

        if (this.props.zscoredata1 != undefined && this.props.zscoredata1.length > 0 ){
            for (let i = 0; i < this.props.zscoredata1[0].length; i++){
                
                chart1Labels.push(this.props.zscoredata1[0][i][0])
                chart1data.push(this.props.zscoredata1[0][i][1])
            }
            // chart1Labels.push(this.props.zscoredata1[i][0])
            // chart1data.push(this.props.zscoredata1[i][1])



            // chart2Labels.push(this.props.zscoredata2[i][0])
            // chart2data.push(this.props.zscoredata2[i][1])
    
        }

        if (this.props.zscoredata2 != undefined && this.props.zscoredata2.length > 0 ){
            for (let i = 0; i < this.props.zscoredata2[0].length; i++){
                
                chart2Labels.push(this.props.zscoredata2[0][i][0])
                chart2data.push(this.props.zscoredata2[0][i][1])
            }
            // chart1Labels.push(this.props.zscoredata1[i][0])
            // chart1data.push(this.props.zscoredata1[i][1])



            // chart2Labels.push(this.props.zscoredata2[i][0])
            // chart2data.push(this.props.zscoredata2[i][1])
    
        }


        const zscoredata1 = {
            labels: chart1Labels,
            datasets: [
              {
                label: 'My First dataset',
                backgroundColor: "#0099CC",
                borderColor: 'rgba(255,99,132,1)',
                borderWidth: 1,
                hoverBackgroundColor: 'rgba(0,153,204,0.4)',
                hoverBorderColor: 'rgba(255,99,132,1)',
                data: chart1data
              }
            ]
          }

          const zscoredata2 = {
            labels: chart2Labels,
            datasets: [
              {
                label: 'My First dataset',
                backgroundColor: "#0099CC",
                borderColor: 'rgba(255,99,132,1)',
                borderWidth: 1,
                hoverBackgroundColor: 'rgba(0,153,204,0.4)',
                hoverBorderColor: 'rgba(255,99,132,1)',
                data: chart2data
              }
            ]
          }
        
          bars.push(
          
          
          <div className="barchart">
              {this.props.sentence1}
          <Bar
            data={zscoredata1} options = {{
                legend: {
                  display: false
               }}}
            
          /></div>)

          bars.push(<div className="barchart">{this.props.sentence2}<Bar
            data={zscoredata2} options = {{
                legend: {
                  display: false
               }}}
            
            
          /> </div>)
        if (this.props.sentences != undefined && this.props.sentences.length > 0 ){
        for (let i = 0 ; i < 2; i++ ){
            things.push( <div className="scatterChart">  {this.props.sentences[i]}  <Scatter data={this.props.data[i]} options={this.props.option[i]} width={"100px"} height={"100px"}/></div> )
        }
    }


        return(
                <div className="chart">
                    
                    
                    {bars}
                    {things}
                    
                    






                </div>


        )
    }
}

export default Charts;