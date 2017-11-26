import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';

export default class VideoModal extends React.Component {
  state = {
    open: false,
    disabled: false,
    buttonText: "Add Feedback",
  };

  handleOpen = () => {
    this.setState({open: true});
  };

  handleClose = () => {
    this.setState({open: false});
    this.props.resetState();
  };

  componentWillReceiveProps(nextProps){
    if(nextProps.close){
      this.handleClose()
    }
  }

  render() {
    const actions = [
      <FlatButton
        label="Cancel"
        primary={true}
        onClick={this.handleClose}
      />,
      // <FlatButton
      //   label="Submit"
      //   primary={true}
      //   onClick={(event) => {
      //     this.props.submit(event)
      //     this.handleClose()
      //     this.setState({disabled: true, buttonText: "Feedback Added"})
      //   }}
      // />,
    ];

    return (
      <div>
        <RaisedButton label={this.props.text} onClick={this.handleOpen} disabled={this.props.disabled}/>
        <Dialog
          title="Add Feedback"
          actions={actions}
          modal={true}
          open={this.state.open}
        >
          {this.props.children}
        </Dialog>
      </div>
    );
  }
}
