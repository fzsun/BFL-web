<template>
<form v-on:change="emit()" class="params">
    <div>
        <div class="label centerAlign">Cost Info</div>
        <div class="flexWrap">
            <div class="field">
                <label class="label">Interest Rate</label>
                <div class="control tooltip is-tooltip-bottom" data-tooltip="Used to approximate time value of money for equipment">
                    <input class="input" type="text" v-model="model.interest_rate">
                </div>
            </div>
            <div class="field">
                <label class="label">Insurance Rate</label>
                <div class="control tooltip is-tooltip-bottom" data-tooltip="Used to acount for additional costs">
                    <input class="input" type="text" v-model="model.insurance_rate">
                </div>
            </div>
            <div class="field">
                <label class="label">Tax Rate</label>
                <div class="control tooltip is-tooltip-bottom" data-tooltip="Used to acount for additional costs">
                    <input class="input" type="text" v-model="model.tax_rate">
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
                <label class="label">Base Infield Cost ($/Mg/km)</label>
                <div class="control tooltip is-tooltip-bottom" data-tooltip="Base hauling cost of in-field transfer per Mg per km.">
                    <input class="input" type="text" v-model="model.cost.base_infield">
                </div>
            </div>
            <div class="field">
                <label class="label">Base Highway Cost</label>
                <div class="control tooltip is-tooltip-bottom" data-tooltip="Base hauling cost of highway transfer per Mg per km.">
                    <input class="input" type="text" v-model="model.cost.base_highway">
                </div>
            </div>
        </div>
    </div>
    <div>
        <div class="label centerAlign makeFull">Farm and Crop Info</div> 
        <div class="flexWrap">
            <div class="field">
                <label class="label">Moisture</label>
                <div class="control tooltip is-tooltip-bottom" data-tooltip="Proportion of water content wet biomass.">
                    <input class="input" type="number" v-model="model.moisture">
                </div>
            </div>
            <ListInput 
                v-bind:list='model.field.area_ratio' 
                v-on:listChange='model.field.area_ratio = $event'
                v-bind:label="'Farm Size Ratio'"
                v-bind:tooltips='tooltips.areaRatio'
            ></ListInput>
        </div>
    </div>
    <div>
        <div class="label centerAlign makeFull">Equipment Configuration Info</div>
        <div class="flexWrap">
            <EquipmentField
                v-bind:list='model.cost.equipment.loadout'
                v-on:listChange='model.cost.equipment.loadout = $event'
                v-bind:label="'Loadout'"
                v-bind:tooltips="tooltips.equipmentFields"
            >
            </EquipmentField>
            <EquipmentField
                v-bind:list='model.cost.equipment.press'
                v-on:listChange='model.cost.equipment.press = $event'
                v-bind:label="'Press'"
                v-bind:tooltips="tooltips.equipmentFields"
            >
            </EquipmentField>
            <EquipmentField
                v-bind:list='model.cost.equipment.chopper'
                v-on:listChange='model.cost.equipment.chopper = $event'
                v-bind:label="'Chopper'"
                v-bind:tooltips="tooltips.equipmentFields"
            >
            </EquipmentField>
            <EquipmentField
                v-bind:list='model.cost.equipment.bagger'
                v-on:listChange='model.cost.equipment.bagger = $event'
                v-bind:label="'Bagger'"
                v-bind:tooltips="tooltips.equipmentFields"
            >
            </EquipmentField>
            <EquipmentField
                v-bind:list='model.cost.equipment.module_former'
                v-on:listChange='model.cost.equipment.module_former = $event'
                v-bind:label="'Module Former'"
                v-bind:tooltips="tooltips.equipmentFields"
            >
            </EquipmentField>
            <EquipmentField
                v-bind:list='model.cost.equipment.module_hauler'
                v-on:listChange='model.cost.equipment.module_hauler = $event'
                v-bind:label="'Module Hauler'"
                v-bind:tooltips="tooltips.equipmentFields"
            >
            </EquipmentField>
        </div>
    </div>

    <div>
        <div class="label centerAlign makeFull">Transportation Factors</div>
        <div class="flexWrap">
            <div class="control tooltip is-tooltip-bottom" data-tooltip="Factor of compression configuration on base hauling cost.">
                <div class="field">
                    <label class="label">Compressed</label>
                    <input 
                        class="input" 
                        type="text" 
                        v-model="model.cost.transport_coef.compressed"
                    >
                </div>
            </div>
            <div class="control tooltip is-tooltip-bottom" data-tooltip="Factor of whole stalk configuration on base hauling cost.">
                <div class="field">
                    <label class="label">Whole Stalk</label>
                    <input 
                        class="input" 
                        type="number" 
                        v-model="model.cost.transport_coef.whole_stalk"
                    >
                </div>
            </div>
            <div class="control tooltip is-tooltip-bottom" data-tooltip="Factor of in module configuration on base hauling cost.">
                <div class="field">
                    <label class="label">In Module</label>
                    <input 
                        class="input" 
                        type="number" 
                        v-model="model.cost.transport_coef.in_module"
                    >
                </div>
            </div>
        </div>
    </div>
    
    <div>
        <div class="label centerAlign">Degradation Factors</div>
        <div class="flexWrap">
            <div class="field">
                <label class="label">Whole Stalk</label>
                <div class="control tooltip is-tooltip-bottom" data-tooltip="Number of weeks until fully degraded for configuration">
                    <input 
                        class="input" 
                        type="number" 
                        v-model="model.degrade.whole_stalk"
                    >
                </div>
            </div>
            <div class="control tooltip is-tooltip-bottom" data-tooltip="Number of weeks until fully degraded for configuration">
                <label class="label">Chopped</label>
                <input 
                    class="input" 
                    type="number" 
                    v-model="model.degrade.chopped"
                >
            </div>
            <div class="control tooltip is-tooltip-bottom" data-tooltip="Number of weeks until fully degraded for configuration">
                <label class="label">In Bunker</label>
                <input 
                    class="input" 
                    type="number" 
                    v-model="model.degrade.in_bunker"
                >
            </div>
            <div class="control tooltip is-tooltip-bottom" data-tooltip="Number of weeks until fully degraded for configuration">
                <label class="label">In Bag</label>
                <input 
                    class="input" 
                    type="number" 
                    v-model="model.degrade.in_bag"
                >
            </div>
        </div>
    </div>
   
</form>
</template>

<script>
import ListInput from './ListInput'
import EquipmentField from './EquipmentField'

export default {
    props: {
        model: {
            type: Object
        }
    },
    components: {
        'ListInput': ListInput,
        'EquipmentField': EquipmentField
    },
    methods: {
        emit() {
            this.$emit('formChange', this.model)
        }
    },
    data() {
        return {
            tooltips: {
                areaRatio: ["Smallest size factor", "Largest size factor"],
                equipmentFields: [
                    "Purchase Cost ($)",
                    "Liftime (yrs) ",
                    "Salvage Value ($)",
                    "Operation Cost ($)",
                    "Capacity (Mg/Week)"
                ]
            }
        }
    }
}
</script>

<style>

.makeFull {
    width: calc(100vw - 4rem);
}

.degradeParams .flexCols {
    width: 18rem;
}

.flexCols {
    display: flex;
    flex-direction: column;
}

.flexWrap {
    display: flex;
    flex-wrap: wrap;
}

.label {
    text-align: left;
}

.centerAlign {
    text-align: center;
    margin: 1rem 0;
}

.section {
    margin-bottom: 1rem;
}
</style>
