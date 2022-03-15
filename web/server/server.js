const express = require('express');
const fs = require("fs");

const app = express();
const PORT = 8080;

app.get('/', (req, res) => {
    res.sendFile('index.html', {root: 'web'});
});

let strategyFile = "strategy.json";
let avgStrategyFile = "avg_strategy.json";
let historiesPayoffsFile = "histories_payoffs.json";

// process arguments
process.argv.forEach(function (val, index, array) {
    if (val.startsWith('--strategy_file')) {
        strategyFile = val.split('=')[1];
    }
    else if (val.startsWith('--avg_strategy_file')) {
        avgStrategyFile = val.split('=')[1];
    }
    else if (val.startsWith('--histories_payoffs_file')) {
        historiesPayoffsFile = val.split('=')[1];
    }
});

const webServer = app.listen(process.env.PORT || PORT, () => {
    console.log(`SERVER: express server is up at PORT=${PORT}! with the following config`)
    const config = {
        port: PORT,
        strategyFile: strategyFile,
        avgStrategyFile: avgStrategyFile,
        historiesPayoffsFile: historiesPayoffsFile,
    }
    console.log(config);
});

app.use(express.static('web'));

app.get('/strategy', (req, res) => {
    const data = JSON.parse(fs.readFileSync(strategyFile));
    res.json(data);
});

app.get('/averageStrategy', (req, res) => {
    const data = JSON.parse(fs.readFileSync(avgStrategyFile));
    res.json(data);
});

app.get('/historiesPayoffs', (req, res) => {
    const data = JSON.parse(fs.readFileSync(historiesPayoffsFile));
    res.json(data);
});
