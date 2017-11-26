import React, { Component } from 'react';
import Category from './Category.js'
import Demo from './Demo'
import Stats from './Stats'
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import * as Actions from '../actions/Actions'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import AppBar from 'material-ui/AppBar';
import Drawer from 'material-ui/Drawer';
import FlatButton from 'material-ui/FlatButton';
import Modal from './Modal';
import Login from './Login';


class App extends Component {

  state = {
    view : "",
    open: false,
    loaded: false,
  }

  proceed = (view) => {
    this.setState({view})
  }

  setUser = (user) => {
    this.setState({user})
  }

  changeView = (newView) => {
    this.setState({view: newView})
  }

  currView(){
    switch (this.state.view) {
      case "Demo":
        return <Demo {...this.props}/>
      case "Stats":
        return <Stats {...this.props}/>
      default:
        return <Demo {...this.props}/>
    }
  }

  handleToggle = () => this.setState({open: !this.state.open});
  handleClose = () => this.setState({open: false});

  render() {

    return (
      <MuiThemeProvider>
        <div>
          <AppBar
            title="Music Genre Classification"
            titleStyle={{textAlign: 'center'}}
            style={{marginTop: "-0.6%"}}
            showMenuIconButton={true}
            onLeftIconButtonTouchTap={()=>this.handleToggle()}
            // iconElementRight={<FlatButton label="Login/Register"/>}
          />
          <div>
          <Drawer
            docked={false}
            open={this.state.open}
            onRequestChange={(open) => this.setState({open})}
            >
            <Category open={this.state.menu} changeView={this.changeView}/>
          </Drawer>
          </div>
          <div>
            {this.currView()}
          </div>
        </div>
      </MuiThemeProvider>
    );
  }
}

function mapStateToProps(state) {
  return state
}

function mapDispatchToProps(dispatch) {
  return {
    	actions: bindActionCreators(Actions, dispatch)
    };
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(App);
