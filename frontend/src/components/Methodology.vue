<template>
<div class="content">
    <br></br>
    <div class="title is-2"> Background</div>
    <br></br>
    <div class="columns is-centered">
        <div class="column is-3">
            <div class="subtitle is-3"> Demand For Bio-Fuels</div>
            <div class="paragraph"> 
                The Energy Independence and Security Act (EISA) of 2007 in the U.S. established a minimum volume 
                of renewable fuels required for blending with fossil fuel to be 36 billion gallons by 2022, and 44.4%
                of that amount must be produced from cellulosic ethonol in the U.S. in order to achieve the desired
                reduction in greenhouse gas emissions in the transportation sector. Given this legislation, a conservative
                estimate will see the bio-fuel market cap at around 80 billion US dollars. <br></br>
            </div>
        </div>
        <div class="column is-3">
        <div class="subtitle is-3">Sorghum</div>
        <div class="paragraph">
            Sorghum is a type of grass that can be used to create cellulosic based bio-fuels. It has an annual 
            harvest of give give or take 13 weeks usually falling within of the 30th and 40th weeks of the year. Sorghum is best
            grown in warm or tropical environments. It requires a soil temperature of 65&#176; and after germanation
            has the potential to be killed off by a frost. Sorghum typically needs between 400-600mm of rainfall
            and should be spaced with an optimal planting density of approximately 120,000 plants per hectare. <br></br>
        </div>
        </div>
        <div class="column is-3">
        <div class="subtitle is-3"> Simulation-Optimization Methodology </div>
        <div class="paragraph"> 
            The value of the sim-Op methodology is it can create an optimal solution while still being verified in
            a stochastic environment to emmulate a real world logistics problem. In our tool we utilize a hub and spoke
            mixed integer program that solves for both the tactical and strategic decision associated with farmgate 
            operations associated with sorghum. The simulation uses random variables based on the parameters to add a 
            degree of variability to the processing rates of equipment and harvest yields. Since the optimization creates 
            a solution that is a pull system, if the processing rates are lower than what is expected, effectiveness of 
            solutions is variable. The sim-op methodology will highlight this result and let you revise your parameters
            so that you can create a solution feasible for a real world operation.  
        </div>
        </div>
    </div>
</div>
</template>

<script>
export default {

}
</script>

<style>
.content {
    text-align: left;
}

.paragraph{
    font-size: 24px
}
</style>
