<template>
  <div id="app">
    <h3>Fill the prioritization form</h3>
    <b-form @submit.prevent="submit">
      <b-form-group
        id="input-group-1"
        label="Test Folder"
      >
        <b-form-file
          v-model="subject"
          no-traverse
          directory
          multiple
          placeholder="Choose the test folder or drop it here..."
          drop-placeholder="Drop the test folders here..."
          accept=".java"
          @change="uploadFiles($event)"
        >
          <template
            slot="file-name"
            slot-scope="{ names }"
          >
            <b-badge variant="dark">
              {{ names[0] }}
            </b-badge>
            <b-badge
              v-if="names.length > 1"
              variant="dark"
              class="ml-1"
            >
              + {{ names.length - 1 }} More files
            </b-badge>
          </template>
        </b-form-file>
      </b-form-group>

      <b-form-group
        id="input-group-2"
        label="Entity"
        label-for="input-2"
      >
        <b-form-select
          id="input-2"
          v-model="entity"
        >
          <option
            disabled
            value=""
          >
            Please select one
          </option>
          <option>bbox</option>
          <option>function</option>
          <option>branch</option>
          <option>line</option>
        </b-form-select>
      </b-form-group>

      <b-form-group
        id="input-group-2"
        label="Algorithm"
        label-for="input-3"
      >
        <b-form-select
          id="input-3"
          v-model="algorithm"
        >
          <option
            disabled
            value=""
          >
            Please select one
          </option>
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

      <b-form-group
        id="input-group-2"
        label="Repetitions"
        label-for="input-4"
      >
        <b-form-input
          id="input-4"
          v-model.number="repetitions"
          type="number"
          placeholder="Enter the repetitions"
        />
      </b-form-group>

      <b-button
        id="button-1"
        pill
        type="submit"
        variant="dark"
        @Click.prevent="submit"
      >
        Execute
      </b-button>
    </b-form>
  </div>
</template>
<script>
import axios from 'axios'

const client = axios.create({ baseURL: 'http://127.0.0.1:3000' })

export default {
  data () {
    return {
      subject: [],
      entity: '',
      algorithm: '',
      repetitions: 1
    }
  },
  methods: {
    uploadFiles: function (event) {
      const path = '/upload'

      const formData = new FormData()
      const files = event.target.files

      for (let i = 0; i < files.length; i++) {
        formData.append('file[]', files[i], files[i].name)
      }

      client.post(path, formData)
        .then(response => {
          console.log(response)
        })
        .catch(err => {
          console.log(err)
        })
    },

    submit: function () {
      const path = '/fastprioritize'
      console.log(this.subject)
      console.log(this.entity)
      console.log(this.algorithm)
      console.log(this.repetitions)

      client.post(path, {
        entity: this.entity,
        algorithm: this.algorithm,
        repetitions: this.repetitions
      })
        .then(response => {
          console.log(response)
        })
        .catch(err => {
          console.log(err)
        })
    }
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
h3 {
  margin-left:40%;
  margin-top:20px;
  font-family: 'Castoro', serif;
}
#input-group-2 {
  margin-left:25%;
  margin-bottom: 20px;
  width:50%;
  padding-left:80px;
  font-weight:bold;
}
#button-1 {
margin-left:50%;
}
.nav-bar {
  padding-left: 50px;;
}
.link {
  padding-right:100px;
  font-size: 20px;
  color:white;
}
</style>
