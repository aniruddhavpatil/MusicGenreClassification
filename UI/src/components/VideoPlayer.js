import React, { Component , Image} from 'react';
import ReactPlayer from 'react-player';
import api from '../api';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import RaisedButton from 'material-ui/RaisedButton';
import {RadioButton, RadioButtonGroup} from 'material-ui/RadioButton';
import TextField from 'material-ui/TextField';
import VideoModal from './VideoModal';

let allTags = ['phone', 'seatbelt']

const styles={
  radioButton: {
    // flex: 1,
  }
}

export default class VideoPlayer extends Component{
  constructor(props){
    super(props);
    this.state = {
      textBox: 0,
      bool: ["false","false"],
      url: null,
      playing: false,
      volume: 0.8,
      muted: false,
      played: 0,
      loaded: 0,
      duration: 0,
      playbackRate: 1.0,
      tenCount: 1,
      validSubmit: false,
      currStart: 0,
      currEnd: 0,
      duration: 0,
      modal: true,
      completed: false,
      disabled: false,
      buttonText: "Add Feedback"
  }
  }

  resetState = () => {
    this.setState(
      {
        textBox: 0,
        bool: ["false","false"],
        url: null,
        playing: false,
        volume: 0.8,
        muted: false,
        played: 0,
        loaded: 0,
        duration: 0,
        playbackRate: 1.0,
        tenCount: 1,
        validSubmit: false,
        currStart: 0,
        currEnd: 0,
        duration: 0,
        modal: true,
        completed: false,
    }
    )
  }

  load = url => {
    this.setState({
      url,
      played: 0,
      loaded: 0
    })
  }

  async send(){
    let tags = []
    console.log("bool",this.state.bool)
    for(let i = 0; i < allTags.length; i++){
      if(this.state.bool[i] == 'true'){
        tags.push(allTags[i])
        // console.log("tags",tags)
      }
    }
    // console.log("tags",tags)
    try{
      const params = {
        id: this.props.id,
        rating: parseFloat(this.state.textBox),
        tags: tags,
        startFrame: this.state.currStart,
        endFrame: this.state.currEnd,
        done: true,
        user: this.props.user,
      }
      let res = await api.post(api.Urls.submitFeedback,params)
      // console.log(res)
      // this.setState({bool: ["false","false"]})
    }catch(error){
      console.log(error)
    }
  }

  componentWillMount(){
    // console.log("id",this.props.id)

  }

  submit = (event) =>{
    // console.log(this.state.bool, this.state.textBox)
    this.send()
    event.preventDefault();
    let fps = parseFloat(this.props.fps)
    let dur = parseFloat(this.state.duration)
    let finalFrame = Math.round(fps * dur)
    this.setState({currStart: this.state.currEnd+1});
    this.setState({modal: false});
    if(this.state.currEnd === finalFrame){
      // console.log("YAHHA");
    }
    this.props.reRender(this.props.id)

  }

  changeBool = (i,val) => {
    let temp = this.state.bool
    temp[i] = val
    this.setState({bool: temp})
    this.validate()
  }

  changeText = (event, newValue) => {
    this.setState({textBox: newValue}, () => this.validate())
  }

  onSeekChange = e => {
    this.setState({ played: parseFloat(e.target.value) }, console.log(this.state.played))
  }

  onPlay = () => {
    this.setState({ playing: true })
  }
  onPause = () => {
    this.setState({ playing: false })
  }

  handlePause = (played) => {
    let secs = played.playedSeconds

    if(secs > this.state.tenCount * 10 && Math.round(secs % 10) == 0){
      this.setState({playing: false, tenCount: Math.round(secs/10) + 1},
        () => {
          console.log('stop',this.state.playing,this.state.tenCount)
          let start = this.state.currStart
          let end = Math.round(secs*this.props.fps)
          console.log(end);
          this.setState({currEnd: end}, ()=> {console.log(this.state.currStart,this.state.currEnd)});

        }
      )
    }
  }

  handleEnd = () => {
    let fps = parseFloat(this.props.fps)
    let dur = parseFloat(this.state.duration)
    let finalFrame = Math.round(fps * dur)
    this.setState({currStart: this.state.currEnd+1},
      () => this.setState({currEnd: finalFrame, completed: true},
      () => console.log(this.state.currStart,this.state.currEnd)
    )
  )
  }

  validate = () => {
    let flag = true
    let rating = parseInt(this.state.textBox)
    console.log("validate", rating);
    if(rating === null || isNaN(rating)) flag = false
    if(rating <= 0  || rating > 5) flag = false
    this.setState({validSubmit: flag})
  }

  render(){
    // console.log(this.state.bool)
    console.log(this.state.disabled)
    return(
      <div style={{flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', borderWidth: 2, padding: '1%'}}>
        <div style={{flex: 1}}>
          <ReactPlayer width={'90%'} style={{}} key={this.props.key} url={this.props.url}  controls />
          {/* <img src={require('../media/yourName.jpg')} style={{width: '40%', height: '80%'}} /> */}
        </div>
        <VideoModal resetState={this.resetState} close={!this.state.modal} disabled={this.state.disabled} text={this.state.buttonText}>
          <div style={{flex: 1}}>
            <ReactPlayer
              playing={this.state.playing}
              width={'100%'}
              key={this.props.key}
              url={this.props.url}
              onSeek={e => console.log('onSeek', e)}
              onPlay={this.onPlay}
              onPause={this.onPause}
              progressFrequency={100}
              onProgress={(played,loaded) => this.handlePause(played)}
              onDuration={duration => this.setState({ duration })}
              onEnded = {() => this.handleEnd()}
              controls
            />
          </div>
        <div style={{flex: 1}}>
          {/* <form onSubmit={(event) => this.submit(event)}> */}
            <div>
            <TextField
              hintText="Rating"
              onChange={(event,newValue)=> this.changeText(event,newValue)}
            />
            {/* <TextField hintText={Math.round(this.props.fps)}/> */}
            </div>

            <Bool question="Using phone?" index={0} changeBool={this.changeBool} />
            <Bool question="Using seatbelt?" index={1} changeBool={this.changeBool} />
            {/* <RaisedButton
              // label="Submit"
              >
              <input type="submit" value="Submit"
                // style={{
                //           cursor: 'pointer',
                //           position: 'absolute',
                //           top: 0,
                //           bottom: 0,
                //           right: 0,
                //           left: 0,
                //           width: '100%',
                //           opacity: 0,
                //       }}
              />
            </RaisedButton> */}
          {/* </form> */}
          <RaisedButton
            label="Submit"
            disabled={!this.state.validSubmit}
            primary={true}
            onClick={(event) => {
              this.submit(event)
              this.onPlay()
              this.setState({validSubmit: false,disabled: true, buttonText: "Feedback Added"})
            }}
          />
        </div>
      </VideoModal>
      </div>
    );
  }
}

class Bool extends Component{

  render(){
    return(
      <label>
        {this.props.question}
        <RadioButtonGroup name="shipSpeed1" defaultSelected="not_light" onChange={(event)=>{
          this.props.changeBool(this.props.index,event.target.value)}}
          // style={{display: 'flex', flexDirection: 'row', flex: 1}}
          >
          <RadioButton
            value="true"
            label="Yes"
            // style={styles.radioButton}
          />
          <RadioButton
            value="false"
            label="No"
            style={styles.radioButton}
          />
        </RadioButtonGroup>
      </label>
    );
  }
}
