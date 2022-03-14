async function loadData(filename) {
    let response = await fetch('./' + filename); //(with path)
    let json = await response.json();
    return json;
}

// a bunch of colors for the players
const COLORS = [
    'rgb(255, 99, 132)',
    'rgb(54, 162, 235)',
    'rgb(75, 192, 192)',
    'rgb(153, 102, 255)',
    'rgb(255, 159, 64)',
    'rgb(255, 205, 86)',
    'rgb(201, 203, 207)',
]

function preprocessData(rawData, time) {
    const REVERSED_NAMES = ['player', 'color', 'iter'];
    // names = attribute in data besides the reserved ones
    let names = Object.keys(rawData[0]).filter(function (d) {
        return REVERSED_NAMES.indexOf(d) === -1; // not in REVERSED_NAMES
    });
    // filter to include only the data for the current time
    rawData = rawData.filter(function (d) {
        return d.iter == time;
    });
    // get the list of unique players
    let players = rawData.map(function (d) {
        return d.player;
    }).filter(function (d, i, self) {
        return self.indexOf(d) === i;
    });
    // color for each player, add to rawData
    rawData.forEach(function (d) {
        d.color = COLORS[players.indexOf(d.player)];
    });
    return {names: names, players: players, rawData: rawData};
}

function plotTernary(data, elt) {


    Plotly.react(elt, [{
        type: 'scatterternary',
        mode: 'markers',
        a: data.rawData.map(function (d) {return d[data.names[0]];}),
        b: data.rawData.map(function (d) {return d[data.names[1]];}),
        c: data.rawData.map(function (d) {return d[data.names[2]];}),
        text: data.rawData.map(function (d) {return d.player;}),
        color: data.rawData.map(function (d) {return d.color;}),
        marker: {
            color: data.rawData.map(function (d) {return d.color;}),
            size: 14,
            line: {width: 2}
        },
    }],
        {
            ternary: {
                aaxis: makeAxis(data.names[0], 0),
                baxis: makeAxis('<br>' + data.names[1], 45),
                caxis: makeAxis('<br>' + data.names[2], -45),
            },
        });

    function makeAxis(title, tickangle) {
        return {
            title: title,
            titlefont: {size: 20},
            tickangle: tickangle,
            tickfont: {size: 15},
            tickcolor: 'rgba(0,0,0,0)',
            ticklen: 5,
            showline: true,
            showgrid: true
        };
    }
}

function plotTriangle(data, elt) {
    let trace = {
        x: data.rawData.map(function (d) {return d[data.names[0]];}),
        y: data.rawData.map(function (d) {return d[data.names[1]];}),
        mode: 'markers',
        marker: {
            size: 14,
            color: data.rawData.map(function (d) {return d.color;}),
        }
    };

    let layout = {
        xaxis: {
            range: [0, 1],
            zeroline: false,
            title: data.names[0],
        },
        yaxis: {
            range: [0, 1],
            showgrid: false,
            title: data.names[1],
        },
        width: 500,
        height: 500,
        shapes: [
            {
                type: 'path',
                path: 'M 0 0 L 0 1 L 1 0 Z',
                // fillcolor: 'rgba(44, 160, 101, 0.5)',
                line: {
                    color: 'rgb(44, 160, 101)'
                }
            },
        ]
    };

    Plotly.react(elt, [trace], layout);
}

function plotGraph(rawData, elt, time) {
    let data = preprocessData(rawData, time);
    let n_actions = data.names.length;
    switch (n_actions) {
        case 3:
            plotTernary(data, elt);
            break;
        case 2:
            plotTriangle(data, elt);
            break;
        default:
            alert("Error: number of actions " + n_actions + " not supported");
    }
}
let strategy = await loadData('strategy.json');
let averageStrategy = await loadData('avg_strategy.json');
// loop through data to get the maximum iter value using reduce
let maxIter = strategy.reduce(function (a, b) {
    return Math.max(a, b.iter);
}, 0);

document.getElementById("rangeSlider").max = maxIter;
plotGraph(strategy, "strategy", 0);
plotGraph(averageStrategy, "avg_strategy", 0);

let updateLoopTime;
let updateLoopGraph;

let refreshRates = [10, 100, 500, 750, 1000];
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
    plotGraph(strategy, "strategy", currentTime);
    plotGraph(averageStrategy, "avg_strategy", currentTime);
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
    document.getElementById("speedOutput").innerHTML = "Speed: " + speed;
});

document.getElementById("speedUp").addEventListener("click", function () {
    refreshRateIndex = Math.max(refreshRateIndex - 1, 0);
    clearInterval(updateLoopTime);
    clearInterval(updateLoopGraph);
    updateLoopTime = setInterval(updateTime, refreshRates[refreshRateIndex]);
    updateLoopGraph = setInterval(updateGraph, refreshRates[refreshRateIndex]);
    let speed = (refreshRates[medianRefreshRateIndex] / refreshRates[refreshRateIndex]).toPrecision(2);
    document.getElementById("speedOutput").innerHTML = "Speed: " + speed;
});
