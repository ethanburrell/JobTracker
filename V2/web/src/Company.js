import React from "react";
import SearchAppBar from "./NavBar.js"


class Company extends React.Component {
//<h1> {this.props.name} </h1>
render() {
  return (
    <div>
    <SearchAppBar />
    <img src={"https://logo.clearbit.com/linkedin.com"} />
    <h1> {this.props.path} </h1>

    <div style={{backgroundColor: "green"}}>
      <h1> $ 36 </h1>
    </div>


    </div>
  );
  }
}

export default Company;
