export default function selectCommande(currentRound, buffer) {
    let stockage = []
    let cond = true
    for (var j = 0; j < 4; j++){
        cond = true
        for (var i = 0; i < buffer.length; i++){
            console.log("boucle1", currentRound+j, buffer[i][0], buffer[i][1])
            if (currentRound+j === buffer[i][0]){
                stockage.push(buffer[i][1])
                cond = false
                console.log("order", buffer[i][1])
            }
        }
        if (cond === true){
            stockage.push(0)
            console.log("pas de commande")
        }
    }
    console.log("a", stockage)
    return stockage
}