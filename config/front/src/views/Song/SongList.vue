<template>
    <v-container>
        <v-container>
            <EasyDataTable
                :headers="headers"
                :items="songs"
                @expand-row="selectSong"
                table-class-name="customize-table"
                show-index
                body-text-direction ="center"
                header-text-direction = "center"
                :hide-rows-per-page="true"
            >
                <template #item-fix="{fix}">
                        <v-chip width="100%" size="small" :color="colors[fix]">{{texts[fix]}}</v-chip>
                </template>
                <template #expand="item">
                    <!-- 선곡모드 :: 추가 링크, 유툽, 뭐.. 줄 선 사람 리스트? 특수 세션 등 -->
                    <v-card class="elevation-0 pa-2">
                        <v-row>
                            <!-- title -->
                            <v-col cols="4">
                                <v-card-title>
                                    <h3>
                                        {{item.title}}
                                    </h3>
                                    <h6>
                                        {{item.artist}}
                                    </h6>
                                </v-card-title>
                                <v-card-text>
                                    <h2> 비고</h2>
                                </v-card-text>
                                <v-card-text class="text-start">
                                    {{item.content}}
                                </v-card-text>
                            </v-col>
                        <v-col>
                            <!-- 비고 -->
                            <h3> 지원하기 </h3>
                            <v-row>
                                <v-col>
                                    <v-select
                                        v-model="selected_position"
                                        :items="item.instruments"
                                        item-title="name"
                                        item-value="name"
                                        label="Position"
                                        density="compact"
                                    ></v-select>
                                </v-col>
                                <v-col>
                                    <v-btn
                                    class="ma-2"
                                    outlined
                                    color="indigo"
                                    @click="applyPosition(item)"
                                    >
                                    Apply!  
                                    </v-btn>

                                </v-col>
                            </v-row>

                            <!-- 세션 지원 및 현황 -->
                                <EasyDataTable
                                    :headers="pos_headers"
                                    :items="item.players"
                                    @click-row="deleteModal"
                                    body-text-direction ="center"
                                    header-text-direction = "center"
                                    :hide-rows-per-page="true"

                                    show-index
                                >
                                    <template #item-name="{player}">
                                        <td>
                                            {{player.name}}
                                        </td>
                                    </template>
                                    <template #item-position="{player}">
                                        <td>
                                            {{player.position}}
                                        </td>
                                    </template>
                                    <template #item-fixed="{fixed}">
                                        <td>
                                            {{fixed}}
                                        </td>
                                    </template>

                                </EasyDataTable>
                        </v-col>
                        </v-row>
                    </v-card>
                    <!-- item마다 확정인지 아닌지를 보여주는 field 필요 -->
                    <!-- <v-card v-else-if="mode==='fix'"> Fix </v-card> -->

                </template>
            </EasyDataTable>
        </v-container>

        <v-dialog v-model ="openModal" >
            <v-card max-width="600px" class="dialog">
                <v-card-title>
                    Quit from {{delFrom.title}}
                </v-card-title>
                <v-card-text>
                    Are you sure to quit from {{delPosition.position}} from {{delFrom.title}}?
                </v-card-text>
                <v-card-actions>
                    <v-btn color="error"  variant="outlined" width="100%" @click="quitPosition">
                        Quit
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-container>


</template>



<script>
import axios from "axios";
import setToken from "@/utils/auth.js"
// import { Header, Item } from "vue3-easy-data-table";

let url = "http://127.0.0.1:8000/api/song/";  // 장고 drf 서버 주소



export default {
    
    name : "SongList",

    data : () => {
        return {

            //songs
            songs : [],
            headers : [
                    {text : 'Artist', value : 'artist'},
                    {text : 'Title', value : 'title'},
                    {text : 'Vocal', value : 'Vocal'},
                    {text : 'Guitar1', value : 'Guitar1'},
                    {text : 'Guitar2', value : 'Guitar2'},
                    {text : 'Bass', value : 'Bass'},
                    {text : 'Drum', value : 'Drum'},
                    {text : 'Keyboard', value : 'Keyboard'},
                    {text : 'Fixed', value : 'fix'},
],
            delFrom : "", // quit from song
            
            // positions
            pos_headers : [
                {text : "Name", value : "name"},
                {text : "Position", value : "position"},
                {text : "Status", value : "fixed"},
            ],
            selected_position : "",
            openModal : false,
            delPosition : "",

            colors : {
                true : "primary",
                false : "error"
            },
            texts : {
                true : "Fixed",
                false : "Not Fixed"
            }

      
        }
    },

    props : ['project'],

    components : {
    },
    
    methods: {
        parsePlayer : function(song){
            song.players.map((player) => {
                console.log(player)
                if (player.fixed){
                    //song[player.position] = player 
                    song[player.player.position] = player.player.user.name 
                }
            })
            return song
        },
        
        songList : function(){
            axios({
                method : "GET",
                url : url,
                headers : setToken(),
                params : {
                    user_id : localStorage.getItem('user'),
                    project_id : this.$route.query.project_id
                }
            }).then((response) => {
                this.songs = response.data.map( (song, index) => {
                    song.index = index
                    song = this.parsePlayer(song)
                    return song
                })

            }).catch((error) => {
                console.log("Failed to get song list", error.response);
            });
        },

        setIndex : function(oldSong, newSong){
            newSong.index = oldSong.index
            newSong = this.parsePlayer(newSong)
            return newSong
        }, 

        to : function(destination){
            this.$router.push({
                name : destination,
                query : {
                    project_id : this.$route.params.project_id
                }})
        },

        applyPosition : function(song){
            axios({
                method : "PATCH",
                url : url + song.id + '/',
                headers : setToken(),
                params : {
                    user_id : localStorage.getItem('user'),
                    position : this.selected_position,
                    action : "apply"
                }
            }).then((response) => {
                this.songs[song.index] = this.setIndex(song, response.data)
            }).catch((error) => {
                console.log("Failed to update song", error.response);
            });
        },

        selectSong : function(index){
            this.delFrom = this.songs[index]
        },

        deleteModal : function(item){
            // item의 user와 현재 user가 같은지?
            if (item.player.user.id === parseInt(localStorage.getItem("user"))){
                this.delPosition = item
                this.openModal = true
            } 
        },

        quitPosition : function(){
            axios({
                method : "PATCH",
                url : url + this.delFrom.id + '/',
                headers : setToken(),
                params : {
                    user_id : localStorage.getItem('user'),
                    position : this.delPosition.player.position,
                    action : "quit"
                }
            }).then((response) => {
                this.openModal = false
                this.songs[this.delFrom.index] = this.setIndex(this.delFrom, response.data)
            }).catch((error) => {
                console.log("Failed to quit from the song", error.response);
            });
        },



    },

    mounted() {
        this.songList()
    },

    watch : {
        project : {
            handler: function(newVal, oldVal){
                newVal;oldVal;
                this.songList()
            },
            deep : true,
            immediate : true,
        },

        songs : {
            handler: function(newVal, oldVal){
                newVal; oldVal
            },
            deep : true,
            immediate : true
        },

    }
}
</script>


<style scoped>
.dialog{
    margin-left: auto!important; margin-right: auto!important; 
}

.customize-table{
    --easy-table-body-item-padding : 0px, 0px;
}
</style>

