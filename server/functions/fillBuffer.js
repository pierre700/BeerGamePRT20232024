import mongoose from "mongoose";
import DBGame from "../model/DBGame.js";

const GameData = mongoose.model("DBGame", DBGame)
let buffer = []

export default function fillBuffer(currentRound, delai, order, buff) {

    console.log(currentRound)
    buffer=buff
    let delaiRound = currentRound + delai
    let arrayBuffer = [delaiRound, order]
    let cond = false
    console.log(currentRound, delai, delaiRound)

    if (buffer.length === 0){buffer.push(arrayBuffer)}

    else{
        for (var j = 0; j < buffer.length; j++){
            if (buffer[j][0] === currentRound + delai){
                cond = true
                buffer[j][1]=buffer[j][1]+order
            }
        }
        }
    if (cond === false){
        buffer.push(arrayBuffer)
        }  
    return buffer  
}

