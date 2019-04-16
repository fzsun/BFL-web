<template>
<div class="field">
    <div class="control"> 
        <form v-on:change="emit()">
            <label class="label">{{label}}</label>
            <div 
                class="flexCols"
            >
                <input 
                    class="input"
                    type="number"
                    v-bind:key="index" 
                    v-for="(item, index) in list"
                    v-model="data[index]"
                    v-bind:placeholder="headers[index]"
                >
            </div>
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
            data: new Array(5),
            showLess: true,
            headers: [
                "Purchase Cost ($)",
                "Liftime (yrs) ",
                "Salvage Value ($)",
                "Operation Cost ($)",
                "Capacity (Mg/Week)"
            ]
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
