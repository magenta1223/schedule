<template>
    <v-container>
        <EasyDataTable
            :headers="headers"
            :items="songs"
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
                    </v-row>
                </v-card>
            </template>
        </EasyDataTable>
    </v-container>


</template>



<script>
import axios from "axios";
import setToken from "@/utils/auth.js"
// import { Header, Item } from "vue3-easy-data-table";

let url = "http://127.0.0.1:8000/api/song/";  // 장고 drf 서버 주소



export default {
    
    name : "SongFixedList",

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
                    console.log(song)
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
                    project_id : this.$route.query.project_id
                }})
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

