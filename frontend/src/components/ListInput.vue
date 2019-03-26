<template>
<div class="field">
    <div class="control"> 
        <form v-on:change="emit()">
            <label class="label">{{label}}</label>
            <input 
                class="input short"
                type="number"
                v-bind:key="item" 
                v-for="(item, index) in list"
                v-model="data[index]"
            >
        </form>
    </div>
</div>
</template>

<script>
export default {
    props: {
        list: {
            type: Array
        },
        label: {
            type: String
        }
    },
    data() {
        return {
            data: Array(this.list.length), 
            // data: this.list
        }
    }, 
    methods: {
        emit() {
            this.$emit('listChange', this.data);
        }
    }
}
</script>

<style>
.short {
    width: 5rem !important;
}
</style>
