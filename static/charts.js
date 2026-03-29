async function loadCharts(){

let res = await fetch("/api/teamstats")
let stats = await res.json()

let labels=[]
let values=[]

stats.slice(0,6).forEach(s=>{
labels.push(s.name)
values.push(parseFloat(s.value))
})

new Chart(document.getElementById("statsChart"),{

type:"bar",

data:{
labels:labels,
datasets:[{
label:"Packers Team Stats",
data:values
}]
}

})

}