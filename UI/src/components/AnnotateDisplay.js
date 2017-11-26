import React, { Component } from 'react';
import api from '../api';
import VideoPlayer from './VideoPlayer';
import Category from './Category.js';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import RaisedButton from 'material-ui/RaisedButton';
import Modal from './Modal';
import TextField from 'material-ui/TextField';



export default class AnnotateDisplay extends Component {

  state={
    vids: [],
    maxVideosPerScreen: 20,
    columns: 4,
    page: 0,
    totalVideos: null,
    list: null,
    totalPages: 1,
    upload: false,
    uploadList: [
      {
        question: "Attention",
        type: "score",
      },
      {
        question: "Phone",
        type: "boolean",
      },
    ],
    file: null,
  }

  update(){
    this.populate(this.state.list);
    console.log('page',this.state.page);
  }

  nextPage(){
    if(this.state.page+1 < this.state.totalPages)
    this.setState({page: this.state.page+1}, this.update)

  }

  prevPage(){
    if(this.state.page > 0)
    this.setState({page: this.state.page-1}, this.update)

  }

  populate(list){
    let file = require('../output.json');

    this.setState({rows: this.state.maxVideosPerScreen/this.state.columns})
    var pageOffset = this.state.page * this.state.maxVideosPerScreen;
    var vids = [];
    for(var row=0; row < this.state.rows; row++){
      var vidRow = [];
      for(var column = 0; column < this.state.columns; column++){
        var rowOffset = row * this.state.columns;
        var videoNumber = pageOffset + rowOffset + column;
        if(videoNumber >= list.length) break;
        // console.log(list[videoNumber])
        // var url = api.Urls.video + list[videoNumber].vid_path.split('/')[6];
        let fileName = ''
        let s = list[videoNumber].vid_path.split('/')
        for(let i = 1;i<s.length;i++)
        {
          if(i == s.length - 1){
            fileName = fileName.concat(s[i])
          }
          else{
            fileName = fileName.concat(s[i]).concat('-d-')
          }
        }
        var url = api.Urls.video + fileName;
        // console.log(url)
        console.log(list[videoNumber]._id.$oid)
        var vidId = list[videoNumber]._id.$oid
        var fps = list[videoNumber].fps
        // console.log(url)
        // console.log("File",file,list[videoNumber].vid_path);

        let rating = "null"

        for(let k = 0 ; k < file.length; k++){
          if( list[videoNumber].vid_path == file[k][0]) rating = file[k][1]
        }

        vidRow.push(
          <div>
            <VideoPlayer key={row * this.state.columns + column} url={url} id={vidId} fps={fps}/>
            <text>{rating}</text>
          </div>
        );
      }

      vids.push(
        <div key={row} style={{flex: 1, display: 'flex',flexDirection: 'row'}}>
          {vidRow}
        </div>
      );
    }
    this.setState({vids}, () => this.render);
  }

  async getData(){
    try{
      const params = {
        user: this.props.username
      }
      let res = await api.post(api.Urls.videolist, params);
      // console.log(JSON.parse(res))
      let arr = []
      if(res != null)
        res.map((item, index)=> arr.push(JSON.parse(item)))
      // console.log(arr)
      if(arr){
        this.populate(arr);
        this.setState({totalVideos: arr.length, list: arr})
        this.setState({totalPages: parseInt(this.state.totalVideos/this.state.maxVideosPerScreen) + ((this.state.totalVideos%this.state.maxVideosPerScreen)===0?0:1)});

      }
    }catch(error){
      console.error(error);
    }
  }

  componentWillMount(){
    this.getData();
  }

  openUpload(){
    this.setState({upload: true});
  }

  closeUpload(){
    this.setState({upload: false});
  }

  fileChange(event){
    alert(event.target.value);
  }



  render() {
    return (

      <MuiThemeProvider>
      <div>

      <div style={{display: 'flex', flexDirection: 'row'}}>
        <div
          // style={{flex: 10}}
          >
            <Modal />
          <div style={{}}>
            {this.state.vids}
          </div>
          <div>
            <TextField value={ "PageNo = " + (this.state.page + 1) + " of  " + (this.state.totalPages)}/>
            <RaisedButton onClick={() => this.prevPage()}>Prev</RaisedButton>
            <RaisedButton onClick={() => this.nextPage()}>Next</RaisedButton>
          </div>
        </div>
          {/* <Modal upload={() => this.upload()} uploadList={this.state.uploadList} /> */}
      </div>
      </div>
    </MuiThemeProvider>
    );
  }
}
