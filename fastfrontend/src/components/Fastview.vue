<template>
<div id="app">

 <h3>Enter your Data</h3>
    <b-form @submit="submit">
      <b-form-group id="input-group-1" label="Subject" label-for="input-1">
        <b-form-textarea
          id="input-1"
          type="text"
          v-model="fastprioritize.subject"
          placeholder="Enter the subject"
        ></b-form-textarea>
      </b-form-group>

      <b-form-group id="input-group-2" label="Entity" label-for="input-2">
        <b-form-select 
          id="input-2"
          v-model="fastprioritize.entity"
        >
          <option disabled value="">Please select one</option>
          <option>bbox</option>
          <option>function</option>
          <option>branch</option>
          <option>line</option>
        </b-form-select>
      </b-form-group>
      
      <b-form-group id="input-group-2" label="Algorithm" label-for="input-3">
        <b-form-select
          id="input-3"
          v-model="fastprioritize.algorithm"
        >
          <option disabled value="">Please select one</option>
          <option>FAST-pw</option>
          <option>FAST-one</option>
          <option>FAST-log</option>
          <option>FAST-sqrt</option>
          <option>FAST-all</option>
          <option>STR</option>
          <option>I-TSD</option>
          <option>ART-D</option>
          <option>ART-F</option>
          <option>GT</option>
          <option>GA</option>
          <option>GA-S</option>
        </b-form-select>
      </b-form-group>

      <b-form-group id="input-group-2" label="Repetitions" label-for="input-4">
        <b-form-textarea
          id="input-4"
          type="number"
          v-model.number="fastprioritize.repetitions"
          placeholder="Enter the repetitions"
          
        ></b-form-textarea>
      </b-form-group>

    <b-button pill v-on:Click="submit" id="button-1" type="submit" variant="dark">Execute</b-button>
     
  </b-form>
    
</div>

</template>
<script>
import axios from 'axios';
export default{
 
  data(){
    return {
       fastprioritize:{
        subject:"",
        entity:"",
        algorithm:"",
        repetitions:1,
      },
    };
  },
  methods:{
    submit:function(){
      const path = 'http://127.0.0.1:3000/fastprioritize'
      axios.post(path, {
        subject:this.fastprioritize.subject,
        entity:this.fastprioritize.entity,
        algorithm:this.fastprioritize.algorithm,
        repetitions:this.fastprioritize.repetitions,
        }
      )
      .then(response => {
        console.log(response);
      })
      .catch(err =>{
        console.log(err);
      });
    },
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Lato&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Castoro&display=swap');
#app {
  font-family: 'Lato', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
#input-group-1 {
  margin-left:25%;
  margin-bottom: 20px;
  width: 50%;
  padding-left: 80px;
  margin-top: 50px;
  font-weight:bold;
 
}
h3{
  margin-left:40%;
  margin-top:20px;
  font-family: 'Castoro', serif;
}
#input-group-2{
  margin-left:25%;
  margin-bottom: 20px;
  width:50%;
  padding-left:80px;
  font-weight:bold;
}
#button-1{
margin-left:50%;
} 
.nav-bar{
  padding-left: 50px;;
}
.link{
  padding-right:100px;
  font-size: 20px;
  color:white;
}
</style>
