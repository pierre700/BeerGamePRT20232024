export default function CalculateNewValues(RoleID, role, NextRole, currentRound, buffer, dmdCli) {
  let
    newStock = role[currentRound].stock,
    newNextStock = NextRole.stock,
    newRetard  = role[currentRound].retard,
    newNextRetard = NextRole.retard,
    currentOrder = 0,
    deliveryValueToNextRole = 0;

  for (var i = 0; i < buffer.length; i++){
    console.log("boucle1", currentRound, buffer[i][1], buffer[i][0])
    if (currentRound === buffer[i][0]){
      currentOrder = buffer[i][1]
      console.log("order", currentOrder)
    }
  }

  //If Stock >= Order
  if (RoleID === 2 | RoleID === 3 | RoleID === 4){
    console.log("if1", newNextStock, currentOrder)
    if(newNextStock >= currentOrder) {
      console.log("if2")
      newStock = newStock + currentOrder
      newNextStock= newNextStock - currentOrder
      if(newNextRetard > 0) {
        console.log("if3")
        //If Retard - Inventory >= 0
        if((newNextRetard - newNextStock) >= 0) {
          console.log("if4")
          newNextRetard = newNextRetard - newNextStock
          newNextStock = 0
        }
        else {
          console.log("else4")
          newNextStock = newNextStock - newNextRetard
          newStock = newStock + newNextRetard
          newNextRetard = 0
        }
      }
    }
    else {
      console.log("else2")
      const diff = currentOrder - newNextStock
      newStock = newStock + newNextStock
      newNextStock = 0
      newNextRetard = newNextRetard + diff
      
    } 
    if (RoleID === 4){
      console.log("if5")
      if (newStock >= dmdCli){
        console.log("if6")
        newStock = newStock - dmdCli
      }
      else {
        console.log("else6")
        newRetard = newRetard - dmdCli + newStock
        newStock = 0
      }
    }
  }
  else {
    console.log("else1", currentOrder)
    newStock = newStock + currentOrder
  }

  role[currentRound].stock = newStock
  NextRole.retard = newNextRetard
  NextRole.stock = newNextStock

  return [role, deliveryValueToNextRole]
}
