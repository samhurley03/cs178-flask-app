let rosterData = []

async function loadRoster(){

let res = await fetch("/api/roster")
rosterData = await res.json()

displayRoster(rosterData)

}


function displayRoster(players){

let container = document.getElementById("rosterCards")
container.innerHTML = ""

players.forEach(p=>{

let card = document.createElement("div")
card.className="playerCard"

card.innerHTML = `

<img src="${p.photo}" width="120">

<h3>${p.name}</h3>

<p>#${p.jersey} | ${p.position}</p>

`

container.appendChild(card)

})

}



document.getElementById("search").addEventListener("input", e=>{

let term = e.target.value.toLowerCase()

let filtered = rosterData.filter(p=>
p.name.toLowerCase().includes(term)
)

displayRoster(filtered)

})


document.getElementById("positionFilter").addEventListener("change", e=>{

let pos = e.target.value

if(pos===""){
displayRoster(rosterData)
return
}

let filtered = rosterData.filter(p=>p.position===pos)

displayRoster(filtered)

})


async function loadSchedule(){

let res = await fetch("/api/schedule")
let games = await res.json()

let table = document.getElementById("scheduleTable")
table.innerHTML=""

games.forEach(g=>{

let row = document.createElement("tr")

row.innerHTML=`

<td>${g.week}</td>
<td>${g.home}</td>
<td>${g.away}</td>
<td>${g.status}</td>

`

table.appendChild(row)

})

}



async function loadScores(){

let res = await fetch("/api/scores")
let games = await res.json()

let table = document.getElementById("scoreTable")

table.innerHTML=""

games.forEach(g=>{

let row=document.createElement("tr")

row.innerHTML=`

<td>${g.away}</td>
<td>${g.awayScore} - ${g.homeScore}</td>
<td>${g.home}</td>
<td>${g.status}</td>

`

table.appendChild(row)

})

}



async function loadTeamStats(){

let res = await fetch("/api/teamstats")

let stats = await res.json()

let table = document.getElementById("teamStats")

table.innerHTML=""

stats.forEach(s=>{

let row=document.createElement("tr")

row.innerHTML=`

<td>${s.name}</td>
<td>${s.value}</td>

`

table.appendChild(row)

})

}

async function liveTracker(){

let res = await fetch("/api/scores")
let games = await res.json()

let packersGame = games.find(g =>
g.home.includes("Packers") || g.away.includes("Packers")
)

if(packersGame){

document.getElementById("packersGame").innerHTML = `
${packersGame.away} ${packersGame.awayScore}
vs
${packersGame.home} ${packersGame.homeScore}
<br>
${packersGame.status}
`

}

}

async function loadLastYearSchedule(){

let res = await fetch("/api/schedule_last_year")

let games = await res.json()

let table = document.getElementById("lastYearSchedule")

table.innerHTML=""

games.forEach(g=>{

let row=document.createElement("tr")

row.innerHTML=`

<td>${g.week}</td>
<td>${g.home}</td>
<td>${g.away}</td>
<td>${g.status}</td>

`

table.appendChild(row)

})

}



function loadAll(){

loadRoster()
loadSchedule()
loadLastYearSchedule()
loadScores()
loadTeamStats()
liveTracker()

}


loadAll()

// AUTO REFRESH EVERY 30 SECONDS
setInterval(loadAll,30000)

