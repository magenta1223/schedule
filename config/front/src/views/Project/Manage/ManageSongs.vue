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
            <template #item-fix="item">
                <v-checkbox  v-model="selectedSongs[item.index]" density="compact" class="cbox"></v-checkbox>
            </template>
            <template #item-delete="item">
                <v-icon :icon="icons.mdiDelete" @click="modal(item)"  density="compact"></v-icon>
            </template>
            <template #expand="item">
                <PlayerSelect
                :song="item"
                @updatePlayers="updatePlayers"
                />
            </template>
        </EasyDataTable>
        <v-dialog v-model ="openModal" >
            <v-card max-width="600px" class="dialog">
                <v-card-title>
                    Delete Song
                </v-card-title>
                <v-card-text>
                    Are you sure to delete {{delItem.title}}?
                </v-card-text>
                <v-card-actions>
                    <v-btn color="error"  variant="outlined" width="100%" @click="deleteSong(delItem)">
                        Delete
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

    </v-container>
</template>



<script>

import axios from "axios";
import setToken from "@/utils/auth.js"
import {mdiDelete} from "@mdi/js"
import PlayerSelect from "@/components/Song/PlayerSelect.vue"

let url = "http://127.0.0.1:8000/api/project/";  // 장고 drf 서버 주소
let song_url = "http://127.0.0.1:8000/api/song/";  // 장고 drf 서버 주소

export default {
    name : "ManageSongs" , 

    data : () => {

        return {
           // project -> props
            project : "",

            //songs -> props
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
                    {text : 'Fix', value : 'fix'},
                    {text : 'Delete', value : 'delete'},
            ],
            
            //manage
            manage_header : [
                {text : "Positions", value : "position"},
                {text : "Select Player", value : "player"},
            ],
            selectedPlayers : {},
            selectedSongs : [],
            openModal : false,
            delItem : {
                name : ''
            },

            icons : {
                mdiDelete
            }
        }
    },

    methods : { 
        parsePlayer : function(song){
            song.players.map((player) => {
                if (player.fixed){
                    song[player.player.position] = player.player.user.name 
                }
            })
            return song
        },
        
        setIndex : function(oldSong, newSong){
            newSong.index = oldSong.index
            newSong = this.parsePlayer(newSong)
            return newSong
        }, 

        retrieveProject : function(){
            axios({
                method : "GET",
                url : url + this.$route.query.project_id + '/',
                headers : setToken(),
                params : {
                    user_id : localStorage.getItem('user'),
                }
            }).then((response) => {
                this.project = response.data
                this.songs = this.project.songs.map( (song, index) => {
                    song.index = index
                    song = this.parsePlayer(song)
                    this.selectedSongs.push(song.fix)
                    return song
                })

                this.status = this.project.status

                if (parseInt(localStorage.getItem('user')) === this.project.leader){
                    console.log("ture")
                    this.manage_mode = true
                }

            }).catch((error) => {
                console.log("Failed to get retreival", error.response);
            });
        },

        updatePlayers : function(selected){
            console.log(this.selectedSongs, selected.players)
            axios({
                method : "PATCH",
                url : song_url + selected.song.id + '/',
                headers : setToken(),
                params : {
                    user_id : localStorage.getItem('user'),
                    selectedPlayers : JSON.stringify(selected.players),
                    action : "fix"
                }
            }).then((response) => {
                this.songs[selected.song.index] = this.setIndex(selected.song, response.data)
                this.manage = false
            }).catch((error) => {
                console.log("Failed to fix this song", error.response);
            });

        

        },


        save : function(){
            this.selectedSongs.map((boolean, song_index)=> {
                this.songs[song_index].fix = boolean
            })
            axios({
                method : "PATCH",
                url : url + this.$route.query.project_id + '/',
                headers : setToken(),
                params : {
                    user_id : localStorage.getItem('user'),
                    project_id :this.$route.query.project_id,
                    selectedSongs : JSON.stringify(this.songs),
                    status : this.status,
                    action : "song"
                }
            }).then((response) => {
                // saved modal 띄우기
                console.log(response)
            }).catch((error) => {
                console.log("Failed to fix the project", error.response);
            });

        },

        modal : function(item){
            this.openModal = true
            this.delItem = item
        },


        deleteSong : function(song){
            song;
            //모달 띄우고 delete view로 걍 보내버리면 됨?> 
            axios({
                method : "DELETE",
                url : song_url + song.id,
                headers : setToken(),
            }).then((response) => {
                response;
                this.openModal = false
                // this.songs에서 지우고 index 다시 세팅
                this.songs.splice(song.index, 1)
                this.selectedSongs.splice(song.index, 1)
                this.songs = this.songs.map( (song, index) => {
                    song.index = index
                    return song
                })
                // saved modal 띄우기
            }).catch((error) => {
                console.log("Failed to delete song", error.response);
            });
        },


    },

    components : {
        PlayerSelect,
    },


    mounted(){
        this.retrieveProject()
    },
    watch : {
        selectedSongs : {
            handler: function(newVal, oldVal){
                newVal;oldVal;
                this.save()
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
    --easy-table-body-row-height : 24px!important;
}


.cbox >>> .v-input__control{
    justify-content: center;
}

.cbox >>> .v-input__details{
    height: 0px!important;
}
</style>