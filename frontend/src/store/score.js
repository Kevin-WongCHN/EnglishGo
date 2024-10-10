import {defineStore} from 'pinia'

export const useScoreStore = defineStore('score', {
    state(){
        return{
            score:0,
            isFinished:false
        }
       
    }
})
