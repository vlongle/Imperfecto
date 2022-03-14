import {
    request, plotStrategyGraph, plotPayoffs, drawGameReplay
} from './utils.js';

let strategy = await request('strategy', []);
let averageStrategy = await request('averageStrategy', []);
let historiesPayoffs = await request('historiesPayoffs', []);

// loop through data to get the maximum iter value using reduce
let maxIter = strategy.reduce(function (a, b) {
    return Math.max(a, b.iter);
}, 0);

document.getElementById("rangeSlider").max = maxIter;
plotStrategyGraph(strategy, "strategy", 0);
plotStrategyGraph(averageStrategy, "avg_strategy", 0);
plotPayoffs(historiesPayoffs, "payoff", 0);
drawGameReplay(historiesPayoffs, "gameReplay", 0);

let updateLoopTime;
let updateLoopGraph;

let refreshRates = [1, 10, 100, 500, 750, 1000];
let medianRefreshRateIndex = Math.floor(refreshRates.length / 2);
let refreshRateIndex = medianRefreshRateIndex;

function updateTime() {
    let currentTime = parseInt(document.getElementById("rangeSlider").value);
    let newTime = currentTime + 1;
    newTime = Math.min(newTime, document.getElementById("rangeSlider").max);
    document.getElementById("rangeSlider").value = newTime;
    document.getElementById("sliderOutput").innerHTML = newTime;
}

function updateGraph() {
    let currentTime = parseInt(document.getElementById("rangeSlider").value);
    plotStrategyGraph(strategy, "strategy", currentTime);
    plotStrategyGraph(averageStrategy, "avg_strategy", currentTime);
    plotPayoffs(historiesPayoffs, "payoff", currentTime);
    drawGameReplay(historiesPayoffs, "gameReplay", currentTime);
}
document.getElementById("start").addEventListener("click", function () {
    updateLoopTime = setInterval(updateTime, refreshRates[refreshRateIndex]);
    updateLoopGraph = setInterval(updateGraph, refreshRates[refreshRateIndex]);
});
document.getElementById("stop").addEventListener("click", function () {
    clearInterval(updateLoopTime);
    clearInterval(updateLoopGraph);
    console.log("stopped");
});

document.getElementById("rangeSlider").addEventListener("change", function () {
    // update output
    document.getElementById("sliderOutput").innerHTML = this.value;
    updateGraph();
});

document.getElementById("rangeSlider").addEventListener("input", function () {
    // update output
    document.getElementById("sliderOutput").innerHTML = this.value;
    updateGraph();
});

document.getElementById("slowDown").addEventListener("click", function () {
    refreshRateIndex = Math.min(refreshRateIndex + 1, refreshRates.length - 1);
    clearInterval(updateLoopTime);
    clearInterval(updateLoopGraph);
    updateLoopTime = setInterval(updateTime, refreshRates[refreshRateIndex]);
    updateLoopGraph = setInterval(updateGraph, refreshRates[refreshRateIndex]);
    let speed = (refreshRates[medianRefreshRateIndex] / refreshRates[refreshRateIndex]).toPrecision(2);
    document.getElementById("speedOutput").innerHTML = "<strong>Speed</strong>: " + speed;
});

document.getElementById("speedUp").addEventListener("click", function () {
    refreshRateIndex = Math.max(refreshRateIndex - 1, 0);
    clearInterval(updateLoopTime);
    clearInterval(updateLoopGraph);
    updateLoopTime = setInterval(updateTime, refreshRates[refreshRateIndex]);
    updateLoopGraph = setInterval(updateGraph, refreshRates[refreshRateIndex]);
    let speed = (refreshRates[medianRefreshRateIndex] / refreshRates[refreshRateIndex]).toPrecision(2);
    document.getElementById("speedOutput").innerHTML = "<strong>Speed</strong>: " + speed;
});
