<template>
<div>
    <div id="s_bfl" class="container section">
        <div class="is-size-4">
            A tool for decision makers to determine the most cost effective 
            way to produce and transport sorghum for use in biofuels. The tool itself
            is an optimization algorithm and simulization that work in tandem to find 
            and test an optimial solution. To learn more about the algorithm 
            <a>see here.</a> 
        </div>
        <br>
        <div class="panel-body">
            <form>
                <vue-form-generator :schema="schema" :model="model" :options="formOptions">
                </vue-form-generator>
            </form>
        </div>
    </div>
</div>
</template>

<script>
import { validators, component as VueFormGenerator } from 'vue-form-generator'

export default {
  components: {
      VueFormGenerator
  },
  data () {
    return {

      model: {
        id: 1,
        name: "John Doe",
        password: "J0hnD03!x4",
        skills: ["Javascript", "VueJS"],
        email: "john.doe@gmail.com",
        status: true
      },

      schema: {
        groups: [
          {
            legend: "User Details",
            fields: [
              {
                type: "input",
                inputType: "text",
                label: "ID (disabled text field)",
                model: "id",
                readonly: true,
                disabled: true
              },
              {
                type: "input",
                inputType: "text",
                label: "Name",
                model: "name",
                id: "user_name",
                placeholder: "Your name",
                featured: true,
                required: true
              },
              {
                type: "input",
                inputType: "email",
                label: "E-mail",
                model: "email",
                placeholder: "User's e-mail address"
              },
              {
                type: "input",
                inputType: "password",
                label: "Password",
                model: "password",
                min: 6,
                required: true,
                hint: "Minimum 6 characters",
                validator: validators.string
              }
            ]
          },
          {
            legend: "Skills & Status",
            fields: [
              {
                type: "select",
                label: "skills",
                model: "type",
                values: ["Javascript", "VueJS", "CSS3", "HTML5"]
              },
              {
                type: "checkbox",
                label: "Status",
                model: "status",
                default: true
              }
            ]
          }
          ],

          formOptions: {
            validateAfterLoad: true,
            validateAfterChanged: true,
            fieldIdPrefix: 'user-'
          }
        }
      }
    }
  }
</script>
