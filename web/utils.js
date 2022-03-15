
/** Request a response from the server
 * @param {string} requestName - the name of the request
 * @param {Array.<Object>} args - the arguments to the request
 *
 * @returns {JSON} the response from the server
 *
 * Example:
 * const data = await request("someRequestName", [arg1, arg2]);
 */
export async function request(requestName, args) {
    let url = '/' + requestName;
    args.forEach(arg => {
        url += `/${arg}`;
    });
    console.log("request: " + url);
    const response = await fetch(url);
    let answer = await response.json();
    return answer;
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

export function preprocessData(rawData, time) {
    const REVERSED_NAMES = ['player', 'color', 'iter'];
    // names = attribute in data besides the reserved ones
    let names = Object.keys(rawData[0]).filter(function (d) {
        return REVERSED_NAMES.indexOf(d) === -1; // not in REVERSED_NAMES
    });
    // filter to includes only the data for the current time
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

export function plotTernary(data, elt) {
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

export function plotStrategyGraph(rawData, elt, time) {
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

export function plotPayoffs(payoffs, elt, time) {
    payoffs = payoffs.filter(function (d) {
        return d.iter <= time;
    });

    let n_players = payoffs[0].payoffs.length;
    var data = [];
    for (let i = 0; i < n_players; i++) {
        let trace = {
            x: payoffs.map(function (d) {return d.iter;}),
            y: payoffs.map(function (d) {return d.payoffs[i];}),
            name: `Player ${i}`,
            type: 'scatter',
            mode: 'lines+markers',
            line: {
                shape: 'spline',
                smoothing: 1.3,
                color: COLORS[i],
                width: 2,
            },
        };
        data.push(trace);
    }

    var layout = {
        legend: {
            y: 0.5,
            font: {size: 16},
            yref: 'paper'
        },
        xaxis: {
            title: 'Iteration',
        },
        yaxis: {
            title: 'Payoff',
        }

    };

    Plotly.react(elt, data, layout);

}

function getActions(histories, time) {
    histories = histories.filter(function (d) {
        return d.iter == time;
    });
    return histories[0].history;
}

function drawGameReplayGeneric(histories, elt, time, gameImageFolder) {
    let actions = getActions(histories, time);
    let html = "";
    for (let i = 0; i < actions.length; i++) {
        html += `<img src="assets/${gameImageFolder}/${actions[i]}.png"
        style="margin: 50px 200px 0px 100px;" height=200, width=200>`;
    }
    let gamePlay = document.getElementById(elt);
    gamePlay.innerHTML = html;
    gamePlay.style.backgroundColor = "orange";
}
function drawRockPaperScissorReplay(histories, elt, time) {
    // append left to the first action, and right to the second action so that
    // images are displayed nicely.
    let histories_copy = JSON.parse(JSON.stringify(histories));
    histories_copy.forEach(function (d) {
        d.history[0] = "left_" + d.history[0];
        d.history[1] = "right_" + d.history[1];
    });
    return drawGameReplayGeneric(histories_copy, elt, time, "rockPaperScissor");
}

function drawPrisonerDilemmaReplay(histories, elt, time) {
    return drawGameReplayGeneric(histories, elt, time, "prisonerDilemma");
}

function drawBarCrowdingReplay(histories, elt, time) {
    return drawGameReplayGeneric(histories, elt, time, "barCrowding");
}

export function drawGameReplay(histories, elt, time) {
    let actions = histories[0].history;
    if (actions.includes("ROCK") || actions.includes("PAPER") || actions.includes("SCISSORS")) {
        drawRockPaperScissorReplay(histories, elt, time);
    } else if (actions.includes("SNITCH") || actions.includes("SILENCE")) {
        drawPrisonerDilemmaReplay(histories, elt, time);
    } else if (actions.includes("STAY_HOME") || actions.includes("GO_TO_BAR")) {
        drawBarCrowdingReplay(histories, elt, time);
    } else {
        alert("Error: game not supported");
    }
}
