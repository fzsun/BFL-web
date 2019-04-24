<template>
<div class="field">
    <label class="label">{{label}}</label>
    <form class="flexWrap" v-on:change="emit()">
        <div
            class="control tooltip is-tooltip-bottom"
            v-bind:data-tooltip="tooltips[index]"
            v-bind:key="index" 
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

.width {
    width: 18rem;
}

.flexWrap {
    display: flex;
    flex-wrap: wrap;
}
</style>
