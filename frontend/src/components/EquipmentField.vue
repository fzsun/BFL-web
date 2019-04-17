<template>
<div class="field">
    <label class="label">{{label}}</label>
    <form v-on:change="emit()">
        <div 
            class="control tooltip is-tooltip-bottom"
            v-bind:key="index" 
            v-bind:data-tooltip="tooltips[index]"
            v-for="(item, index) in list"
        >
            <input 
                class="input"
                type="number"
                v-model="data[index]"
            >
        </div>
    </form>
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
        },
        tooltips: {
            type: Array
        }
    },
    data() {
        return {
            data: this.list,
            showLess: true,
        }
    }, 
    methods: {
        emit() {
            this.$emit('listChange', this.data);
        },
        showAll() {
            this.showLess = !this.showLess;
        }
    }
}
</script>

<style>

.flexCols {
    display: flex;
    /* flex-direction: column; */
}
</style>
