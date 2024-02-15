import mongoose from "mongoose";

import DBGame from "../model/DBGame.js";
import CalculateNewValues from "../functions/CalculateNewValues.js";
import fillBuffer from "../functions/fillBuffer.js";

export default function UpdateGame(io, socket, intData) {
    const room = intData.gameCode
    const role = intData.selectedRole
    const orderValue = intData.orderValue
    const producerDelay = parseInt(intData.producerDelay)
    const distributorDelay = parseInt(intData.distributorDelay)
    const wholesalerDelay = parseInt(intData.wholesalerDelay)
    const retailerDelay = parseInt(intData.retailerDelay)
    const GameData = mongoose.model("DBGame", DBGame)
    console.log(producerDelay, distributorDelay, wholesalerDelay, retailerDelay)


    GameData.findOne({ gameCode: room }, (err, data) => {
        if(err) return console.log("Erreur: " + err)

        if(data === null) return console.log("Aucun enregistrement trouvé")

        let producer = data.roundData.producer
        let distributor = data.roundData.distributor
        let wholesaler = data.roundData.wholesaler
        let retailer = data.roundData.retailer
        let MJ = data.roundData.MJ
        const currentRound = data.roundData.currentRound
        let bufferProducer = []
        let bufferDistributor = []
        let bufferWholesaler = []
        let bufferRetailer = []


        if(data.roundData.currentRound === 0) {
            switch (role) {
                case 1:
                    producer.push({
                        stock: data.gameSettings.startStock,
                        order: parseInt(orderValue),
                        retard: 0
                    })
                    break
                case 2:
                    distributor.push({
                        stock: data.gameSettings.startStock,
                        order: parseInt(orderValue),
                        retard: 0
                    })
                    break
                case 3:
                    wholesaler.push({
                        stock: data.gameSettings.startStock,
                        order: parseInt(orderValue),
                        retard: 0
                    })
                    break
                case 4:
                    retailer.push({
                        stock: data.gameSettings.startStock,
                        order: parseInt(orderValue),
                        retard: 0
                    })
                    break
                case 5: 
                    MJ.push({
                        prodDelay: producerDelay,
                        distrDelay:distributorDelay,
                        wholeDelay: wholesalerDelay,
                        retailDelay: retailerDelay
                    })
                    break
            }
        }
        else {
            switch (role) {
                case 1:
                    producer.push({
                        stock: producer[currentRound-1].stock,
                        order: parseInt(orderValue),
                        retard: producer[currentRound-1].retard
                    })
                    break
                case 2:
                    distributor.push({
                        stock: distributor[currentRound-1].stock,
                        order: parseInt(orderValue),
                        retard: distributor[currentRound-1].retard
                    })
                    break
                case 3:
                    wholesaler.push({
                        stock: wholesaler[currentRound-1].stock,
                        order: parseInt(orderValue),
                        retard: wholesaler[currentRound-1].retard
                    })
                    break
                case 4:
                    retailer.push({
                        stock: retailer[currentRound-1].stock,
                        order: parseInt(orderValue),
                        retard: retailer[currentRound-1].retard
                    })
                    break
                case 5: 
                    MJ.push({
                        prodDelay: producerDelay,
                        distrDelay: distributorDelay,
                        wholeDelay: wholesalerDelay,
                        retailDelay: retailerDelay
                    })
                    break
            }
        }
        //console.log(MJ[currentRound].prodDelay, data.roundData.MJ, data.gameSettings.startStock)
        let rounds = [producer.length, distributor.length, wholesaler.length, retailer.length, MJ.length]
        let checkIfDataCanBeCommitted = true
        rounds.map(element => {
            if(element !== data.roundData.currentRound+1 || element === []) checkIfDataCanBeCommitted = false
        })
        //Les données peuvent être distribuées une fois que tous les joueurs ont passé des commandes pour le tour en cours
        if(checkIfDataCanBeCommitted) {


            const selectedDemandB = data.gameSettings.selectedDemand
            const constDemandB = data.gameSettings.constDemand
            const minDemandB = data.gameSettings.minDemand
            const maxDemandB = data.gameSettings.maxDemand
            const rampCoeffB = data.gameSettings.rampCoeff
            const rampShiftB = data.gameSettings.rampShift
            const sinCoeffB = data.gameSettings.sinCoeff
            const sinFreqB = data.gameSettings.sinFreq
            const sinPhaseB = data.gameSettings.sinPhase
            const sinShiftB = data.gameSettings.sinShift

            let values = [], delivery = 0, demandClient=0

            if (currentRound === 0){
                bufferProducer = []
                bufferDistributor = []
                bufferWholesaler = []
                bufferWholesaler = []
            }
            else{
                bufferProducer = data.roundData.buffer[currentRound-1].bufferProd
                bufferDistributor = data.roundData.buffer[currentRound-1].bufferDistr
                bufferWholesaler = data.roundData.buffer[currentRound-1].bufferWhole
                bufferRetailer = data.roundData.buffer[currentRound-1].bufferRetail
            }

            bufferProducer = fillBuffer(currentRound, MJ[currentRound].prodDelay, producer[currentRound].order, bufferProducer)
            bufferDistributor = fillBuffer(currentRound, MJ[currentRound].distrDelay, distributor[currentRound].order, bufferDistributor)
            bufferWholesaler = fillBuffer(currentRound, MJ[currentRound].wholeDelay, wholesaler[currentRound].order, bufferWholesaler)
            bufferRetailer = fillBuffer(currentRound, MJ[currentRound].retailDelay, retailer[currentRound].order, bufferRetailer)

            data.roundData.buffer.push({
                bufferProd: bufferProducer, 
                bufferDistr: bufferDistributor,
                bufferWhole: bufferWholesaler,
                bufferRetail: bufferRetailer
            })


            console.log(bufferProducer, bufferDistributor, bufferWholesaler, bufferRetailer)

            values = CalculateNewValues(1, producer, distributor[currentRound], currentRound, bufferProducer, false)
            producer = values[0]
            delivery = values[1]

            values = CalculateNewValues(2, distributor, producer[currentRound], currentRound, bufferDistributor, false)
            distributor = values[0]
            delivery = values[1]

            values = CalculateNewValues(3, wholesaler, distributor[currentRound], currentRound, bufferWholesaler, false)
            wholesaler = values[0]
            delivery = values[1]

        if(selectedDemandB===0){
            //Constant demand
            demandClient = constDemandB
        }
        else if(selectedDemandB===1){
            //Random demand between min and max values
            demandClient = Math.floor(Math.random() * (maxDemandB - minDemandB) ) + minDemandB
        }
        else if(selectedDemandB===2){
            //Ramp value of equation y=a*t+b
            //Todo: If calculated demand is negative, put the demand at 0
            demandClient = rampCoeffB*currentRound+rampShiftB
        }
        else if(selectedDemandB===3){
            //Sinus value of equation y=a*sin(2*pi*f*t+p)+b
            //Todo: If calculated demand is negative, put the demand at 0
            demandClient = Math.round(sinCoeffB*Math.sin(2*3.14*sinFreqB*currentRound+sinPhaseB)+sinShiftB)
        }
        values=CalculateNewValues(4, retailer, wholesaler[currentRound], currentRound, bufferRetailer, demandClient)
        retailer = values[0]
        delivery = values[1]

            data.roundData.currentRound++
            data.roundData.producer = producer
            data.roundData.distributor = distributor
            data.roundData.wholesaler = wholesaler
            data.roundData.retailer = retailer
            data.roundData.demandClient = demandClient
            data.roundData.demandClientList.push(demandClient)
            data.markModified("roundData")
            data.save()
            io.to(room).emit("update_player_data", data)
        }
        else {
            data.roundData.producer = producer
            data.roundData.distributor = distributor
            data.roundData.wholesaler = wholesaler
            data.roundData.retailer = retailer
            data.save()
        }
    })
}
