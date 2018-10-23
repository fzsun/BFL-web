<template>
<div>
    <div class="tabs">
        <ul>
            <li v-for="tab in tabs" v-bind:class="{'is-active': tab.isActive}" :key="tab">
            <a @click="selectTab(tab)">
                {{ tab.name }}
            </a>
            </li>
        </ul>
    </div>
    <div class="tab-details">
        <slot></slot>
    </div>
</div>
</template>

<script>
export default {
    data() {
        return {
        tabs: [],
        }
    },
    created() {
        this.tabs = this.$children;
    },
    methods: {
        selectTab(selectedTab) {
        this.tabs.forEach(
        function(tab){
            tab.isActive = (selectedTab.name == tab.name)
        }
        ) 
        }
    }
}
</script>

<style>

</style>
