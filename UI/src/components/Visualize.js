import React, {Component} from 'react';
import AnnotateDisplay from './AnnotateDisplay';

class Visualize extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <AnnotateDisplay />
      </div>
    );
  }
}

export default Visualize;
