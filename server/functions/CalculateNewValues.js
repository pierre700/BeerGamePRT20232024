export default function CalculateNewValues(RoleID, role, currentRound, buffer, nextBuffer, dmdCli, commandeRecue) {
  let
    newStock = role[currentRound].stock,
    newRetard  = role[currentRound].retard,
    order = 0,
    nextOrder = 0,
    somme = 0,
    dispo = 0;

  if (RoleID === 1){
    for (var i = 0; i < buffer.length; i++){
      console.log("boucle1", currentRound, buffer[i][1], buffer[i][0])
      if (currentRound === buffer[i][0]){
        commandeRecue = buffer[i][1]
        //console.log("order", currentOrder)
      }
    }
  }
  /*if (RoleID === 4){
    newRetard = 0
    nextOrder = dmdCli
  }
  else{
  */
  for (var i = 0; i < nextBuffer.length; i++){
    //console.log("boucle1", currentRound, nextBuffer[i][1], nextBuffer[i][0])
    if (currentRound === nextBuffer[i][0]){
      nextOrder = nextBuffer[i][1]
      //console.log("order", currentOrder)
    }
  }
  somme = newStock + commandeRecue - newRetard - nextOrder
  console.log("somme", somme, newStock, commandeRecue, newRetard, nextOrder)
  if (somme >= 0){
    dispo = newRetard + nextOrder
    newStock = somme
    newRetard = 0
  }
  else{
    dispo = newStock + order
    newStock = 0
    newRetard = 0 - somme
  }
  role[currentRound].stock = newStock
  role[currentRound].retard = newRetard
  return [role, dispo]
  
}
