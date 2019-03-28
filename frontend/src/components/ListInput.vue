<template>
<div class="field">
    <div class="control"> 
        <form v-on:change="emit()">
            <label class="label">{{label}}</label>
            <div v-if="showLess" class="flexCols">
                <input 
                    class="input"
                    type="number"
                    v-bind:key="index" 
                    v-for="(item, index) in list.slice(0,2)"
                    v-model="data[index]"
                >
            </div>
            <div v-if="!showLess" class="flexCols">
                <input 
                    class="input"
                    type="number"
                    v-bind:key="index" 
                    v-for="(item, index) in list"
                    v-model="data[index]"
                >
            </div>
            <button type="button" v-on:click="showAll()">
                <span v-if="showLess">show all</span>
                <span v-if="!showLess">show less</span>
            </button>
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
    flex-direction: column;
}
</style>
