<template>
<div class="field">
    <div class="control"> 
        <form v-on:change="emit()">
            <label class="label">{{label}}</label>
            <div v-if="showLess">
                <input 
                    class="input"
                    type="number"
                    v-bind:key="index" 
                    v-for="(item, index) in list"
                    v-model="data[index]"
                    v-bind:placeholder="placeHolders[index]"
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
        },
        placeHolders: {
            type: Array
        }
    },
    data() {
        return {
            data: new Array(this.list.length),
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
</style>
