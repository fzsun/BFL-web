<template>
<form v-on:change="emit()" class="params">
    <div>
        <div class="label centerAlign">Cost Info</div>
        <div class="flexWrap">
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
        </div>
    </div>
    <div class="field">
        <label class="label">Moisture</label>
        <div class="control">
            <input class="input" type="number" v-model="model.moisture">
        </div>
    </div>
    <ListInput 
        v-bind:list='model.field.area_ratio' 
        v-on:listChange='model.field.area_ratio = $event'
        v-bind:label="'Farm Size Ratio'"
        v-bind:placeHolders='placeHolders.areaRatio'
    ></ListInput>
    <!-- <div class="field">
        <label class="label">Price per Mg</label>
        <div class="control">
            <input class="input" type="text" v-model="model.price">
        </div>
    </div> -->
    
    <div>
        <div class="label centerAlign">Equipment Configuration Info</div>
        <div class="flexWrap">
            <EquipmentField
                v-bind:list='model.cost.equipment.loadout'
                v-on:listChange='model.cost.equipment.loadout = $event'
                v-bind:label="'Loadout'"
            >
            </EquipmentField>
            <EquipmentField
                v-bind:list='model.cost.equipment.press'
                v-on:listChange='model.cost.equipment.press = $event'
                v-bind:label="'Press'"
            >
            </EquipmentField>
            <EquipmentField
                v-bind:list='model.cost.equipment.chopper'
                v-on:listChange='model.cost.equipment.chopper = $event'
                v-bind:label="'Chopper'"
            >
            </EquipmentField>
            <EquipmentField
                v-bind:list='model.cost.equipment.bagger'
                v-on:listChange='model.cost.equipment.bagger = $event'
                v-bind:label="'Bagger'"
            >
            </EquipmentField>
            <EquipmentField
                v-bind:list='model.cost.equipment.module_former'
                v-on:listChange='model.cost.equipment.module_former = $event'
                v-bind:label="'Module Former'"
            >
            </EquipmentField>
            <EquipmentField
                v-bind:list='model.cost.equipment.module_hauler'
                v-on:listChange='model.cost.equipment.module_hauler = $event'
                v-bind:label="'Module Hauler'"
            >
            </EquipmentField>
        </div>
    </div>
    <div class="transCoefficients">
        <label class="label">Transportation Factors</label>
        <div class="flexCols">
            <input 
                class="input" 
                type="text" 
                v-model="model.cost.transport_coef.compressed"
                placeholder="Compressed"
            >
        </div>
        <div class="flexCols">
            <input 
                class="input" 
                type="text" 
                v-model="model.cost.transport_coef.whole_stalk"
                placeholder="Whole Stalk"
            >
        </div>
        <div class="flexCols">
            <input 
                class="input" 
                type="text" 
                v-model="model.cost.transport_coef.in_module"
                placeholder="In Module"
            >
        </div>
    </div>
    
    <div>
        <div class="label centerAlign">Degradation Factors</div>
        <div class="flexWrap">
            <!-- Add <br>, Finish labeling, swap trans factors, remedy placeholder vs default  -->
            <div class="field">
                <label class="label">Whole Stalk</label>
                <div class="control">
                    <input 
                        class="input" 
                        type="number" 
                        v-model="model.degrade.whole_stalk"
                    >
                </div>
            </div>
            <div class="control">
                <input 
                    class="input" 
                    type="number" 
                    v-model="model.degrade.chopped"
                >
            </div>
            <div class="control">
                <input 
                    class="input" 
                    type="number" 
                    v-model="model.degrade.in_bunker"
                >
            </div>
            <div class="control">
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
            placeHolders: {
                areaRatio: ["Smallest", "Largest"],
            }
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

.degradeParams .flexCols {
    width: 18rem;
}

.params .input {
  width: 18rem;
  margin-right: 1rem;
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
}
</style>
