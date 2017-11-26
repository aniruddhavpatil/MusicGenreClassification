import React, {Component} from 'react';
import MenuItem from 'material-ui/MenuItem';
import RaisedButton from 'material-ui/RaisedButton';


class Category extends React.Component {

  constructor(props) {
    super(props);
    let Menu = [
      this.menuItem("Demo"),
      this.menuItem("Stats"),
    ]
    this.state = {
      menu: Menu
    };
  }
  menuItem = (name) => <MenuItem onClick={()=>this.props.changeView(name)}>{name}</MenuItem>
  render() {
    return (
      <div>
          {this.state.menu}
      </div>
    );
  }
}

export default Category;
