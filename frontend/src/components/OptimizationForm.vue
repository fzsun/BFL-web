<template>
<form v-on:change="emit()" class="params">
    <div class="field">
        <label class="label">Moisture</label>
        <div class="control">
            <input class="input" type="number" v-model="model.moisture">
    </div>
    </div>
    <div class="field">
        <label class="label">Demand (Mg)</label>
        <div class="control">
            <input class="input" type="text" v-model="model.demand">
        </div>
    </div>
    <div class="field">
        <label class="label">Horizon (weeks)</label>
        <div class="control">
            <input class="input" type="text" v-model="model.horizon">
        </div>
    </div>
    <!-- <div class="field">
    <label class="label">Number Farms</label>
    <div class="control">
        <input class="input" type="text" v-model="model.num_fields">
    </div>
    </div>
    <div class="field">
    <label class="label">Number SSL</label>
    <div class="control">
        <input class="input" type="text" v-model="model.demand">
    </div>
    </div> -->
    <ListInput 
        v-bind:list='model.ssl_sizes' 
        v-on:listChange='model.ssl_sizes = $event'
        v-bind:label="'SSL Sizes [small, medium, large]'"
    ></ListInput>
    <div class="field">
        <label class="label">SSL Sizes [small, medium, large]</label>
        <div class="control">
            <input class="input" type="text" v-model="model.ssl_sizes">
        </div>
    </div>
    <div class="field">
        <label class="label">Harvest Progress</label>
        <div class="control">
            <input class="input" type="text" v-model="model.harvest_progress">
        </div>
    </div>
    <div class="field">
        <label class="label">Field - Dry Yield</label>
        <div class="control">
            <input class="input" type="text" v-model="model.field.dry_yield">
        </div>
    </div>
    <div class="field">
        <label class="label">Field - Radius</label>
        <div class="control">
            <input class="input" type="text" v-model="model.field.radius">
        </div>
    </div>
    <div class="field">
        <label class="label">Field - Proportion Devoted</label>
        <div class="control">
            <input class="input" type="text" v-model="model.field.proportion_devoted">
        </div>
    </div>
    <div class="field">
        <label class="label">Field - Area Ratio</label>
        <div class="control">
            <input class="input" type="text" v-model="model.field.area_ratio">
        </div>
    </div>
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
    <div class="field">
        <label class="label">Equipment Loadout Cost</label>
        <div class="control">
            <input class="input" type="text" v-model="model.cost.equipment.loadout">
        </div>
    </div>
    <div class="field">
        <label class="label">Equipment Press Cost</label>
        <div class="control">
            <input class="input" type="text" v-model="model.cost.equipment.press">
        </div>
    </div>
    <div class="field">
        <label class="label">Equipment Chopper Cost</label>
        <div class="control">
            <input class="input" type="text" v-model="model.cost.equipment.chopper">
        </div>
    </div>
    <div class="field">
        <label class="label">Equipment Bagger Cost</label>
        <div class="control">
            <input class="input" type="text" v-model="model.cost.equipment.bagger">
        </div>
    </div>
    <div class="field">
        <label class="label">Equipment Module Former Cost</label>
        <div class="control">
            <input class="input" type="text" v-model="model.cost.equipment.module_former">
        </div>
    </div>
    <div class="field">
        <label class="label">Equipment Module Hauler Cost</label>
        <div class="control">
            <input class="input" type="text" v-model="model.cost.equipment.module_hauler">
        </div>
    </div>
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
  justify-content: space-around;
  flex-wrap: wrap;
}

.params .input {
  width: 20rem;
}
</style>
