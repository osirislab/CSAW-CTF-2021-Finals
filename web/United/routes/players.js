var express = require('express');
const db = require('../db/database');
var router = express.Router();

const get_players = (...args) => {
    return new Promise(resolve => {
        let data = []
        let qry = 'SELECT rowid, first, last, specialty FROM players';
        //var players = [];
    
        if (args.length > 0) {
            qry += ` WHERE rowid = '${args[0]}'`;
        }
        
        
        //let qry = `SELECT rowid, first, last FROM players WHERE rowid = '${args[0]}'`
        console.log(qry);
        
        db.all(qry,[], (err, rows) => {
            if(err) console.log(err);
            if(rows && rows.length >0) rows.forEach((row) => data.push(row));
            resolve(data);
        });
    });
}

router.get('/', async (req,res) => {

    let p = await get_players();
    res.render('player', {
        title: "Player Roster",
        players: p,
        detail: false
    })
    
});

router.get('/:rowid', async (req, res) => { 

    let p = await get_players(req.params.rowid);
    res.render('player', {
        //title: `${p[0].first} ${p[0].last}`,
        title: "Player Roster",
        players: p,
        detail: true
    })
});

module.exports = router;