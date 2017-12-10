import React from 'react';

import { configure, shallow } from 'enzyme';
import Adapter from 'enzyme-adapter-react-15';

import ExampleWork from '../js/example-work';

configure({adapter: new Adapter() });

const myWork = [
  {
    'title': "Work Example",
    'image': {
      'desc': "example screenshot of a project involving code",
      'source': "images/example1.png",
      'comment': ""
    }
  }, {
    'title': "Portfolio Boilerplate",
    'image': {
      'desc': "A Serverless Portfolio",
      'source': "images/example2.png",
      'comment': ""
    }
  }
]

describe("ExampleWork compononent", () => {
  let component = shallow(<ExampleWork work={myWork}/>);  
 
  it("Should be a 'section' element", () => {
    console.log(component.debug());
  });
});
