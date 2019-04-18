<template>
<div>
    <section class="hero is-light is-bold">
        <div class="hero-body">
            <div class="container">
            <h1 class="title">
                Biomass Feedstock Logistics
            </h1>
            <h2 class="subtitle">
                Some introduction about team.
            </h2>
            <router-link class="button is-primary" to="/about">View More</router-link>
            </div>
        </div>
    </section>

    <div class="section columns">

        <div class="column is-4">
            <div class="card">
            <div class="card-image">
                <figure class="image is-3by2">
                <img src="../assets/images/s-bfls.jpg" alt="Placeholder image">
                </figure>
            </div>
            <div class="card-content">
                <p class="title">Sorghum BFLS</p>
                <p>A decision support tool for optimal design of sorghum biomass feedstock supply chains.</p>
            </div>
            <div class="card-content is-bottom">
                <router-link class="button is-primary is-fullwidth" :to="{ name: 'S_BFLS'}">View</router-link>
            </div>
            </div>
        </div>
        <div class="column is-4">
            <div class="card">
                <div class="card-content">
                <div class="content">
                    <p class="title is-4"> Background </p>
                    <p class="paragraph2"> Demand For Bio-Fuels</p>
                    <p class="paragraph">
                        The Energy Independence and Security Act (EISA) of 2007 in the U.S. established a minimum volume 
                        of renewable fuels required for blending with fossil fuel to be 36 billion gallons by 2022, and 44.4%
                        of that amount must be produced from cellulosic ethonol in the U.S. in order to achieve the desired
                        reduction in greenhouse gas emissions in the transportation sector. Given this legislation, a conservative
                        estimate will see the bio-fuel market cap at around 80 billion US dollars. <br></br>
                    </p>
                    <p class="paragraph2">Sorghum</p>
                    <p class="paragraph">
                        Sorghum is a type of grass that can be used to create cellulosic based bio-fuels. It has an annual 
                        harvest of give give or take 13 weeks usually falling within of the 30th and 40th weeks of the year. Sorghum is best
                        grown in warm or tropical environments. It requires a soil temperature of 65&#176; and after germanation
                        has the potential to be killed off by a frost. Sorghum typically needs between 400-600mm of rainfall
                        and should be spaced with an optimal planting density of approximately 120,000 plants per hectare. <br></br>
                    </p>
                    <p class="paragraph2"> Simulation-Optimization Methodology </p>
                    <p class="paragraph"> 
                        The value of the sim-Op methodology is it can create an optimal solution while still being verified in
                        a stochastic environment to emmulate a real world logistics problem. In our tool we utilize a hub and spoke
                        mixed integer program that solves for both the tactical and strategic decision associated with farmgate 
                        operations associated with sorghum. The simulation uses random variables based on the parameters to add a 
                        degree of variability to the processing rates of equipment and harvest yields. Since the optimization creates 
                        a solution that is a pull system, if the processing rates are lower than what is expected, effectiveness of 
                        solutions is variable. The sim-op methodology will highlight this result and let you revise your parameters
                        so that you can create a solution feasible for a real world operation.  
                    </p>
                </div>
                </div>
            </div>
        </div>
        <div class="column is-4">
            <div class="card">
                <div class="card-content">
                    <p class="title is-4"> Sim-Op Tool Description </p>
                    <p class="paragraph2"> Helpful hints for usage: </p>
                    <p class="paragraph">
                        1. In the 1.0 version of our tool, once you choose an equipment configuration and optimize, you cannot 
                        change the configuration without refreshing the browser. If you do change the configuration and attempt
                        to re-optimize, the browser will continue buffering until you return to the appropriate configuration
                        or refresh and start over.<br></br>
                        2. Right click on map pins to remove them.<br></br>
                        3. The optimization is set to a default max run-time of 60 seconds and the simulation will take roughly
                        0-30 seconds. If the process has taken longer, you have run into an infeasible solution. Try adjust parameters
                        (namely number of farms/ssls) to remedy, if this doesn't work then refresh and start from scratch. <br></br>
                        4. To achieve a competitive $/Mg operational cost, it is important to keep your system in a relatively close
                        area. The research our tool is based off utilized a 50 km radius area with 120 farms and 60 potential ssl sites
                        randomly generated. Using these parameters, it was found that a system using forage chop harvest and bunker 
                        ensiling will get you an optimal cost around $36/Mg.
                    </p>  
                </div>
            </div>
        </div>
        <div class="column is-1"></div>

    </div>
</div>
</template>

<style>
.title {
    text-align: center;
}
.paragraph {
    text-align: left;
    font-size: 18px;
}

.paragraph1{
    text-align: left;
    font-size: 20px;
}
.paragraph2 {
    text-align: center;
    font-size: 20px;
}
</style>