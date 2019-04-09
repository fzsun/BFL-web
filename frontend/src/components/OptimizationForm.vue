<template>
<form v-on:change="emit()" class="params">
    <div class="field">
        <label class="label">Moisture</label>
        <div class="control">
            <input class="input" type="number" v-model="model.moisture">
        </div>
    </div>
    <ListInput 
        v-bind:list='model.field.area_ratio' 
        v-on:listChange='model.field.area_ratio = $event'
        v-bind:label="'Area Ratio (Explination)'"
    ></ListInput>
    <div class="field">
        <label class="label">Price per Mg</label>
        <div class="control">
            <input class="input" type="text" v-model="model.price">
        </div>
    </div>
    <div class="field">
        <label class="label">Interest Rate</label>
        <div class="control">
            <input class="input" type="text" v-model="model.interest_rate">
        </div>
    </div>
    <div class="field">
        <label class="label">Insurance Rate</label>
        <div class="control">
            <input class="input" type="text" v-model="model.insurance_rate">
        </div>
    </div>
    <div class="field">
        <label class="label">Tax Rate</label>
        <div class="control">
            <input class="input" type="text" v-model="model.tax_rate">
        </div>
    </div>
    <ListInput 
        v-bind:list='model.cost.equipment.loadout' 
        v-on:listChange='model.cost.equipment.loadout = $event'
        v-bind:label="'Equipment Loadout Cost [Explination, ..., ]'"
    ></ListInput>
    <ListInput 
        v-bind:list='model.cost.equipment.press' 
        v-on:listChange='model.cost.equipment.press = $event'
        v-bind:label="'Equipment Press Cost [Explination, ..., ]'"
    ></ListInput>
    <ListInput 
        v-bind:list='model.cost.equipment.chopper' 
        v-on:listChange='model.cost.equipment.chopper = $event'
        v-bind:label="'Equipment Chopper Cost [Explination, ..., ]'"
    ></ListInput>
    <ListInput 
        v-bind:list='model.cost.equipment.bagger' 
        v-on:listChange='model.cost.equipment.bagger = $event'
        v-bind:label="'Equipment Bagger Cost [Explination, ..., ]'"
    ></ListInput>
    <ListInput 
        v-bind:list='model.cost.equipment.module_former' 
        v-on:listChange='model.cost.equipment.module_former = $event'
        v-bind:label="'Equipment Module Former Cost [Explination, ..., ]'"
    ></ListInput>
    <ListInput 
        v-bind:list='model.cost.equipment.module_hauler' 
        v-on:listChange='model.cost.equipment.module_hauler = $event'
        v-bind:label="'Equipment Module Hauler Cost [Explination, ..., ]'"
    ></ListInput>
    <div class="field">
        <label class="label">Bunker Annual Ownership Cost</label>
        <div class="control">
            <input class="input" type="text" v-model="model.cost.bunker_annual_own">
        </div>
    </div>
    <div class="field">
        <label class="label">SSL Annual Ownership Cost</label>
        <div class="control">
            <input class="input" type="text" v-model="model.cost.ssl_annual_own">
        </div>
    </div>
    <div class="field">
        <label class="label">Base Infield Cost</label>
        <div class="control">
            <input class="input" type="text" v-model="model.cost.base_infield">
        </div>
    </div>
    <div class="field">
        <label class="label">Base Highway Cost</label>
        <div class="control">
            <input class="input" type="text" v-model="model.cost.base_highway">
        </div>
    </div>
    <div class="field">
        <label class="label">Transportation Coefficient - Compressed</label>
        <div class="control">
            <input class="input" type="text" v-model="model.cost.transport_coef.compressed">
        </div>
    </div>
    <div class="field">
        <label class="label">Transportation Coefficient - Whole Stalk</label>
        <div class="control">
            <input class="input" type="text" v-model="model.cost.transport_coef.whole_stalk">
        </div>
    </div>
    <div class="field">
        <label class="label">Transportation Coefficient - In Module</label>
        <div class="control">
            <input class="input" type="text" v-model="model.cost.transport_coef.in_module">
        </div>
    </div>
    <div class="field">
        <label class="label">Whole Stalk Degrade</label>
        <div class="control">
            <input class="input" type="text" v-model="model.degrade.whole_stalk">
        </div>
    </div>
    <div class="field">
        <label class="label">Chopped Degrade</label>
        <div class="control">
            <input class="input" type="text" v-model="model.degrade.chopped">
        </div>
    </div>
    <div class="field">
        <label class="label">In Bunker Degrade</label>
        <div class="control">
            <input class="input" type="text" v-model="model.degrade.in_bunker">
        </div>
    </div>
    <div class="field">
        <label class="label">In Bag Degrade</label>
        <div class="control">
            <input class="input" type="text" v-model="model.degrade.in_bag">
        </div>
    </div>
    <div class="field">
        <label class="label">Configurations</label>
        <div class="control">
            <input class="input" type="text" v-model="model.configurations">
        </div>
    </div>
</form>
</template>

<script>
import ListInput from './ListInput'

export default {
    props: {
        model: {
            type: Object
        }
    },
    components: {
        'ListInput': ListInput
    },
    methods: {
        emit() {
            this.$emit('formChange', this.model)
        }
    },
    data() {
        return {
            // model = this.defaultModel
        }
    }
}
</script>

<style>
.params {
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;
}

.params .input {
  width: 18rem;
  margin-right: 1rem;
}
</style>
