<template>
<div>
    <!-- This is where html gets written -->
    <div class="title">This is a Vue Template File</div>

    <!-- 
        Here we use the ListInput component written in 
        another part of our code. We use v-bind to bind a value
        from the data section to the list prop in the the ListInput
        component. We then use v-on to tell the ListInput to bind
        to userInput whenever the input is changed. After, that we use
        v-bind twice more to pass data into the component.
    -->
    <ListInput 
        v-bind:list='list' 
        v-on:listChange='userInput = $event'
        v-bind:label="'Example List Input'"
        v-bind:tooltips='exampleTooltips'
    ></ListInput>
</div>
</template>

<script>
import ListInput from './ListInput'

export default {
    // props are objects that you can pass into a child element 
    // Template.vue would be a child of whatever component it is imported into
    props: {
        model: {
            type: Object
        }
    },
    // Components are other .vue files that can be added to your code so that you don't
    // have to write the same code twice. You import components at the time of the file
    // and register them here.
    components: {
        'ListInput': ListInput,
    },
    // Methods are functions you want to be able to access from the template section
    // the allow us to execute commands with data.
    methods: {
        emit() {
            this.$emit('formChange', this.model)
        }
    },
    // data is where declare the variables that you want your code to use
    // and interact with 
    data() {
        return {
            list: ["example", "example", "example"],
            // update list will get stored in this variable
            userInput: [],
            exampleTooltips: ["this is 1", "this is 2", "this is 3"]
        }
    }
}
</script>

<style>
/* 
    this is where css is written. However, try as much as possible not to write 
    your own css because we are using Bulma as our primary style framework. If you don't
    known what that is google "Bulma css" - I'm not your mom. Hopefully mystyles.css 
    still exists at this point.
*/

</style>
