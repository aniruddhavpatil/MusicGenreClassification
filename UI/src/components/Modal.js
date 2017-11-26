import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';
import TextField from 'material-ui/TextField';
import {RadioButton, RadioButtonGroup} from 'material-ui/RadioButton';
import LinearProgress from 'material-ui/LinearProgress';
import api from '../api';
import Snackbar from 'material-ui/Snackbar';
import CircularProgress from 'material-ui/CircularProgress';

const styles = {
  button: {
    margin: 12,
  },
  exampleImageInput: {
    cursor: 'pointer',
    position: 'absolute',
    top: 0,
    bottom: 0,
    right: 0,
    left: 0,
    width: '100%',
    opacity: 0,
  },
};

export default class Modal extends React.Component {
  state = {
    open: false,
    file: null,
    fileName: null,
    uploadList: this.props.uploadList,
    uploadStatus: false,
    debug: null,
    debugError: null,
    completed: 0,
    genre: null,
    hideButton: false,
    recoData: [],
  };

  async uploadDone(filename){
    try{
      const params = {
        filename: this.state.fileName
      }
      let res = await api.post(api.Urls.uploadDone,params);
      console.log('Hwllo',res)
      this.setState({genre: res.genre})
      this.setState({uploadStatus: true})
      this.getReco(this.state.fileName)
    }catch(error){
      console.error(error);
    }
  }

  async getReco(filename){
    try{
      const params = {
        filename: this.state.filename,
        genre: this.state.genre
      }
      let res = await api.post(api.Urls.reco,params)
      console.log(res)
      this.setState({recoData: res.reco})
    }catch(error){
      console.error(error)
    }
  }

  something = () => {
    this.setState({uploadStatus: true})
  }
  // async getId

  async upload(){
    this.setState({hideButton: true})
    let percentage = 0
    try{
      let data = new FormData();
      data.append('name', "hello");
      data.append('file', this.state.file);
      console.log(this.state.file)
      let xhr = new XMLHttpRequest();
      let f = this.uploadDone
      let filename = this.state.fileName
      let t = this

      xhr.open('post', api.Urls.upload, true);

      xhr.upload.onprogress = e => {
        if (e.lengthComputable) {
          percentage = (e.loaded / e.total) * 100;
          this.setState({completed: percentage})
          if(percentage === 100) {
            // f(filename,t);
          }
        }
      };

      xhr.onerror = function(e) {
        console.log('Error');
        alert('File upload error')
        console.log(e);
      };
      xhr.onload = function() {
        console.log(this.statusText);
      };

      xhr.send(data);
      // let it = data.entries()
      // console.log(it.next())
      // let res = await api.post(api.Urls.upload,data)
      // console.log(res)
    }catch(error){
      console.log(error)
    }

  }

  handleOpen = () => {
    this.setState({open: true});
  };

  handleClose = () => {
    this.setState({open: false});
  };

  getCards = () => {
    let x = []
    for(let i = 0;i<5;i++){
      x.push(
        <div style={{padding: 10,elevation: 5,borderWidth: 2, borderColor: 'red',alignSelf: 'center',alignItems: 'center',textAlign: 'center'}}>
          <text style={{textAlign: 'center',alignSelf: 'center',marginTop: 20,fontSize: 23}}>
            {this.state.recoData[i]}
          </text>
        </div>
      )
    }
    return x
  }

  render() {
    const actions = [
      <FlatButton
        label="Cancel"
        primary={true}
        onClick={this.handleClose}
      />,
      <FlatButton
        label="Test"
        primary={true}
        onClick={() => this.upload(this.state.file)}
      />,
    ];

    return (
      <div>
        {!this.state.hideButton?
          <div style={{position: 'absolute',alignItems: 'center',top: '50%',left: '46%'}}>
            <RaisedButton label="Choose a music file" onClick={this.handleOpen} />
          </div>
          :
          this.state.genre == null ?
          <div style={{position: 'absolute',top: '50%',left: '50%'}}>
            <CircularProgress size={80} thickness={5} />
          </div>
          :
          <div style={{marginTop: 30,alignSelf: 'center',textAlign: 'center'}}>
            <text style={{fontWeight: 'bold',fontSize: '25',color: 'blue'}}>
              {this.state.genre}
            </text>
            <div style={{textAlign: 'center',alignSelf: 'center',marginTop: 20}}>
              <text style={{fontSize: 25,fontWeight: 'bold'}}>Other songs you might like</text>
            </div>
            {this.getCards()}
          </div>
        }
        <Dialog
          title="Dialog With Actions"
          actions={actions}
          modal={true}
          open={this.state.open}
        >
          <RaisedButton label={"Choose file"}
            labelPosition="before"
            style={styles.button}
            containerElement="label">
            <input style={styles.exampleImageInput} type="file" onChange={ (event) => {
            // console.log(event.target.files[0])
            this.setState({file: event.target.files[0], fileName: event.target.files[0].name},()=>console.log("File",this.state.file))
            }
          }/></RaisedButton>
          <TextField
            value={this.state.fileName}
          />
          {
            this.state.completed == 0?
            null
            :
            <LinearProgress mode="determinate" value={this.state.completed} />
          }
          <Snackbar
              open={this.state.completed == 100}
              message="Upload Complete"
              autoHideDuration={1000}
              onRequestClose={()=> {if(this.state.completed == 100){
                this.uploadDone(this.state.filename)}
                ;this.setState({open: false,completed: 0})}}
            />
          {/* <TextField
            hintText="Rating"
            onChange={(event,newValue)=>this.setState({debug: newValue}, ()=>{if(isNaN(this.state.debug)) this.setState({debugError: "Please enter number"})})}
            errorText={this.state.debugError}
          /> */}
        </Dialog>
      </div>
    );
  }
}
