import React from "react";
import SearchAppBar from "./NavBar.js"
import TextField from '@material-ui/core/TextField';
import InputAdornment from '@material-ui/core/InputAdornment';
import "./style.css"
//
import Input from '@material-ui/core/Input';
import OutlinedInput from '@material-ui/core/OutlinedInput';
import FilledInput from '@material-ui/core/FilledInput';
import InputLabel from '@material-ui/core/InputLabel';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import NativeSelect from '@material-ui/core/NativeSelect';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import ButtonGroup from '@material-ui/core/ButtonGroup';
import ToggleButton from '@material-ui/lab/ToggleButton';
import ToggleButtonGroup from '@material-ui/lab/ToggleButtonGroup';
import Switch from '@material-ui/core/Switch';

import PlusOne from '@material-ui/icons/PlusOne'
import IconButton from '@material-ui/core/IconButton';



class InterviewCycle extends React.Component {
  constructor(props) {
    super(props);
    // Don't call this.setState() here!
    this.state = {
      textfields: [{step: ""}]
    };
  }

  addField = () => {
    var new_arr = this.state.textfields.concat({step: ""})
    this.setState({
      textfields: new_arr
    })
    console.log(this.state.textfields)
  }

  handleLangChange = () => {
    var lang = this.state.textfields;
    //console.log(lang)
    this.props.onSelectLanguage(lang);
  }

  saveText = index => event => {
    //console.log(index)
    //console.log(event.target.value)

    var temp = this.state.textfields
    temp[index].step = event.target.value
    this.setState({
      textfields: temp
    })
    this.handleLangChange();
  }

  render() {
    return (
      <div>
        {this.state.textfields.map((item, i) =>
          <div key={i} >
          {i != 0 && <br />}
          <TextField
            //onChange={this.saveText.bind(i)}
            onChange={this.saveText(i)}
            helperText={"Interview Step " + (i + 1)}
            margin="normal"
            value={this.state.textfields[i].step}
            key={i}
          />
          </div>
        )
        }
        <IconButton
          variant="contained"
          color="primary"
          onClick={this.addField}
          >
          <PlusOne />
        </IconButton>
      </div>
    )
  }
}



class Form extends React.Component {
  constructor(props) {
    super(props);
    // Don't call this.setState() here!
    this.state = {
      checkedPay: false,
      companyName: "",
      positionName: "",
      location: "",
      yearsCollege: 0 ,
      prevIntern: 0,
      school: "",
      focus: "",
      gender: "",
      salary: 0,
      hour_or_month: 0,
      housingStipend: 0,
      Interview_cycle: []
    };
  }
//Green color scheme
  handleChange = () => {
    this.setState({
      checkedPay: ! this.state.checkedPay
    })
  }

  textUpdate = param => event => {
    console.log(param, event.target.value, this.state.param)
    this.setState({
       param: (this.state.param == undefined) ? event.target.value : this.state.param + event.target.value
    })

  }

  handleLanguage = (langValue) => {
    this.setState({Interview_cycle: langValue});
    console.log("handleLanguage", langValue)
  }

  submit = () => {
    //console.log("submit:", this.state.Interview_cycle)
    var cycle = this.state.Interview_cycle

    var arr = []
    cycle.map((item, i) =>
    arr.push(item.step)
    )
    this.setState({
      cycle: arr
    })
    console.log("to return", this.state)



  }

  render() {
    return (
      <div className={"article"}>
        <TextField
          id="standard-helperText"
          label="Company Name"
          //defaultValue="Default Value"
          //helperText="Some important text"
          margin="normal"
          defaultValue={this.state["companyName"]}
          onChange={this.textUpdate("companyName")}
        />
        <br />
      <TextField
        id="standard-helperText"
        label="Position Name"
        margin="normal"
        defaultValue={this.state.positionName}
        onChange={this.textUpdate("positionName")}
      />
      <br />

      <TextField
        id="standard-helperText"
        label="Location"
        margin="normal"
        defaultValue={this.state.location}
        onChange={this.textUpdate("location")}
      />
      <br />
      <TextField
        id="standard-helperText"
        label="Years of Attendance in College"
        margin="normal"
        fullWidth
        defaultValue={this.state.yearsCollege}
        onChange={this.textUpdate("yearsCollege")}
      />
      <br />
      <TextField
        id="standard-helperText"
        label="Number of Previous Internships"
        type="number"
        margin="normal"
        fullWidth
        defaultValue={this.state.prevIntern}
        onChange={this.textUpdate("prevIntern")}
      />
      <br />
      <TextField
        id="standard-helperText"
        label="School"
        margin="normal"
        defaultValue={this.state.school}
        onChange={this.textUpdate("school")}
      />
      <br />
      <FormControl
        //className={classes.formControl}
      >
              <InputLabel>Focus</InputLabel>
              <NativeSelect
                //value={state.age}
                //onChange={handleChange('age')}
                input={<Input name="Focus"/>}
                value={this.state.focus}
                onChange={this.textUpdate("focus")}
              >
                <option value="" />
                <option value={10}>UI</option>
                <option value={20}>Full Stack</option>
                <option value={30}>Backend</option>
                <option value={30}>AI/ML</option>
              </NativeSelect>
              <FormHelperText>Focus of Position</FormHelperText>
            </FormControl>
      <br />


      <FormControl
        //className={classes.formControl}
      >
              <InputLabel>Gender</InputLabel>
              <NativeSelect
                //value={state.age}
                //onChange={handleChange('age')}
                input={<Input name="Gender"/>}
                value={this.state.gender}
                onChange={this.textUpdate("gender")}
              >
                <option value="" />
                <option value={10}>Male</option>
                <option value={20}>Female</option>
                <option value={20}>Other</option>
              </NativeSelect>
              <FormHelperText>Gender</FormHelperText>
            </FormControl>

      <br />
      <br />
      <TextField
        id="filled-adornment-amount"
        //className={clsx(classes.margin, classes.textField)}
        //variant="filled"
        label="Salary"
        type="number"
        //fullWidth
        // value={values.amount}
        // onChange={handleChange('amount')} //onChange={handleChange}>
        InputProps={{
          startAdornment: <InputAdornment position="start">$</InputAdornment>,
        }}
        defaultValue={this.state.salary}
        onChange={this.textUpdate("salary")}
        />



        <Grid component="label" container alignItems="center" spacing={1}>
                  <Grid item>per Hour</Grid>
                  <Grid item>
                    <Switch
                      checked={this.state.checkedPay}
                      onChange={this.handleChange}
                      //value="checkedC"
                      color="default"
                    />
                  </Grid>
                  <Grid item>per Month</Grid>
                </Grid>



  <TextField
    id="filled-adornment-amount"
    //className={clsx(classes.margin, classes.textField)}
    //variant="filled"
    label="Housing Stipend (per Month)"
    type="number"
    //fullWidth
    // value={values.amount}
    // onChange={handleChange('amount')}
    InputProps={{
      startAdornment: <InputAdornment position="start">$</InputAdornment>,
    }}
    defaultValue={this.state.housingStipend}
    onChange={this.textUpdate("housingStipend")}
    />
    <br />
    <br />

    <p> Interview Cycle </p>
    <InterviewCycle onSelectLanguage={this.handleLanguage}/>


    <Button
      variant="contained"
      color="primary"
      onClick={this.submit}
      >
      Submit
    </Button>

    </div>
    );
    }
}


class EntryForm extends React.Component {
//<h1> {this.props.name} </h1>
render() {
  return (
    <div>
      <SearchAppBar />
      <Form />
    </div>

  );
  }
}

export default EntryForm;
