import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import SearchCompanies from "./SearchCompanies.js"
import Company from "./Company.js"
import EntryForm from "./EntryForm.js"


function AmbiguousExample() {
  return (
    <Router>
      <div>


        {/*
          Sometimes you want to have a whitelist of static paths
          like "/about" and "/company" but also allow for dynamic
          patterns like "/:user". The problem is that "/about"
          is ambiguous and will match both "/about" and "/:user".
          Most routers have an algorithm to decide for you what
          it will match since they only allow you to match one
          "route". React Router lets you match in multiple places
          on purpose (sidebars, breadcrumbs, etc). So, when you
          want to clear up any ambiguous matching, and not match
          "/about" to "/:user", just wrap your <Route>s in a
          <Switch>. It will render the first one that matches.
      */}
        <Switch>
          <Route path="/newentry" component={EntryForm} />
          <Route path="/about" component={About} />
          <Route path="/company/:name" component={CompanyRouter} />
        </Switch>
      </div>
    </Router>
  );
}

function About() {
  return <SearchCompanies />;
}

function CompanyRouter({ match }) {
  return (
    <div>
      <Company path={match.params.name}/>
    </div>
  );
}

export default AmbiguousExample;
