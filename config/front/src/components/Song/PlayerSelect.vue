<template>

<v-card class="elevation-0 pa-2">
    <EasyDataTable
        :headers="player_header"
        :items="serialize(song)"
        body-text-direction ="center"
        header-text-direction = "center"
        :hide-rows-per-page="true"
        show-index
    >
        <template #item-player="item">
            <td>
                <v-select
                v-model="selectedPlayers[item.position]"
                :items="item.player"
                item-title="name"
                item-value="id"
                density="compact"
                >      
                          
                </v-select>
            </td>
        </template>
    </EasyDataTable>
    <v-card-actions>
        <v-btn width = "100%" @click="updatePlayers()">
            UPDATE
        </v-btn>
    </v-card-actions>
</v-card>
       
</template>



<script>



export default {
    name : "PlayerSelect" , 

    data : () => {

        return {
            //manage
            player_header : [
                {text : "Positions", value : "position"},
                {text : "Select Player", value : "player"},
            ],
            selectedPlayers : {},
        }
    },

    props : ['song'],

    methods : { 
        serialize : function(item){
            let instruments = {}
            let selectedPlayers = {}
            let players = item.players
            let inst_list = Array()

            console.log(players)

            for (let i in players){
                let songPlayer = players[i]
                let player = songPlayer.player
                let position = player.position
                // instruments 생성
                if (!(position in instruments)){
                    instruments[position] = Array()
                    selectedPlayers[position] = ""
                }
                if (songPlayer.fixed){
                    console.log('playerselect', songPlayer.id)
                    selectedPlayers[position] = songPlayer.id
                }
                instruments[position].push({
                    id : songPlayer.id,
                    name : player.name
                })
            }

            for (let index in item.instruments){
                let position = item.instruments[index]
                inst_list.push({
                    'position' : position,
                    'player' : instruments[position],
                    'selected' : ""
                })
            }

            this.selectedPlayers = selectedPlayers


            return inst_list
        },

        updatePlayers : function(){
            console.log(this.selectedPlayers)
            this.$emit('updatePlayers', { song : this.song, players : this.selectedPlayers })
        },
    },


    mounted(){

    },
    

    // watch : {
    //     selectedPlayers : {
    //         handler : function(newVal, oldVal){
    //             console.log(newVal, oldVal)
    //         },
    //         deep : true,
    //         immediate : true
    //     }
    // }

}
</script>


<style scoped>

.customize-table{
    --easy-table-body-item-padding : 0px, 0px;
    --easy-table-body-row-height : 24px!important;
}
</style>