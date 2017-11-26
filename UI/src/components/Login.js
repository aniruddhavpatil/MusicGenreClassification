import React, { Component } from 'react';
import Dialog from 'material-ui/Dialog';
import RaisedButton from 'material-ui/RaisedButton';
import TextField from 'material-ui/TextField';
import FlatButton from 'material-ui/FlatButton';
import api from '../api';



export default class Login extends Component {

  state = {
    open: false,
    username: "",
    password: "",
  }

  async login(username,password) {
    console.log(username,password);
    try{
      const params = {
        username: username,
        password: password,
      }
      let res = await api.post(api.Urls.login, params)
      if(res.success){
        this.props.actions.setUser(username)
        this.props.proceed('Annotate')
      }
    }
    catch(error){
      console.log(error)
    }
  }

  handleOpen = () => {
    this.setState({open: true});
  };

  handleClose = () => {
    this.setState({open: false});
  };

  fakelogin = (username, password) => {
    console.log(username,password);
    this.props.proceed("Annotate")
  }

  render(){
    const actions = [
      // <FlatButton
      //   label="Cancel"
      //   primary={true}
      //   onClick={this.handleClose}
      // />,
      <FlatButton
        label="Login"
        primary={true}
        onClick={() => this.login(this.state.username, this.state.password)}
      />,
    ];
    return(
      <div>
        {/* <RaisedButton label="Login" onClick={this.handleOpen} /> */}
        {/* <Dialog
          title="Dialog With Actions"
          actions={actions}
          modal={true}
          open={this.state.open}
        > */}
          <div style={{display: 'flex', flexDirection: 'column'}}>
            <TextField
              value={this.state.username}
              hintText="Enter username"
              onChange={(e) => this.setState({username: e.target.value}) }
            />

            <TextField
              value={this.state.password}
              hintText="Enter password"
              type="password"
              onChange={(e) => this.setState({password: e.target.value}) }
            />
            <div>
            <RaisedButton
              label="Login"
              primary={true}
              onClick={() => this.login(this.state.username, this.state.password)}
            />
            </div>
          </div>

        {/* </Dialog> */}
      </div>
    )
  }
}
