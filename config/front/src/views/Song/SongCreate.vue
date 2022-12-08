<template>
    <v-container class = "posting-container">

        <v-row>
            <v-col class ="text-h2 text-start active mb-2"> New Song
            </v-col>
        </v-row>
        <!-- Title -->
        <v-row>
            <v-col> 
                <v-text-field v-model="title" placeholder="Title" name="title" type="text"></v-text-field>
            </v-col>
        </v-row>
        <v-row>
            <v-col> 
                <v-text-field v-model="artist" placeholder="Artist" name="artist" type="text"></v-text-field>
            </v-col>
        </v-row>

        <!-- Content -->
        <!-- Text Editor : TipTap https://uxgjs.tistory.com/220 -->
        <v-row>
            <v-col> 
                <v-textarea
                v-model="content"
                name="input-7-4"
                :value="content"
                ></v-textarea>
            </v-col>
        </v-row>
        <!-- button -->
        <v-row class="text-start">
            <v-col class="btn-container">
                <v-btn
                class="ma-2"
                outlined
                color="indigo"
                @click="createSong()"
                >
                Create!  
                </v-btn>
            </v-col>
        </v-row>

          <v-table>
            <thead>
                <tr>
                    <th class="text-left">
                    Name
                    </th>
                    <th class="text-center">
                    requirement
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr
                    v-for="item in positions"
                    :key="item.name"
                >
                    <td>{{ item.name }}</td>
                    <td class="text-center">
                        <v-btn class = "elevation-0" :icon="icons.mdiMinus" size="small" @click="subtract(item)"></v-btn>
                        {{ item.requirement }} 명
                        <v-btn class = "elevation-0" :icon="icons.mdiPlus" size="small" @click="add(item)">+</v-btn></td>
                </tr>
                <tr>
                    <td>
                        <v-text-field v-model="newPosition" variant="underlined">
                        </v-text-field>
                    </td>
                    <td>
                        <v-btn class="elevation-0" width="100%" @click="addPosition()">
                            Add New Position
                        </v-btn>
                    </td>
                </tr>

            </tbody>
            
        </v-table>

    </v-container>

</template>

<script>
import axios from "axios";
import setToken from "@/utils/auth.js"
import { mdiMinus, mdiPlus  } from '@mdi/js';

let url = "http://127.0.0.1:8000/api/song/";  // 장고 drf 서버 주소

export default {
    
    name : "SongCreate",

    data : () => {
        return {
            title : "",
            artist : "",
            content : "",
            newPosition : "",
            positions: [
                {
                    name: 'Vocal',
                    requirement: 0,
                },
                {
                    name: 'Guitar',
                    requirement: 0,
                },
                {
                    name: 'Bass',
                    requirement: 0,
                },
                {
                    name: 'Drum',
                    requirement: 0,
                },
                {
                    name: 'Keyboard',
                    requirement: 0,
                },
          
        ],
        icons : { 
            mdiMinus, mdiPlus
        }
            }
        },

    components : {
    },
    
    methods: {
        subtract : function(item){
            if (item.requirement - 1 >= 0){
                item.requirement = item.requirement - 1
            }
        },

        add : function(item){
            item.requirement = item.requirement + 1
        },

        addPosition : function(){
            let existingPosition = false
            for (let i in this.positions){
                if (this.positions[i].name === this.newPosition){
                    this.positions[i].requirement += 1
                    existingPosition = true
                }
            }
            
            if (!existingPosition){
                this.positions.push({
                    name : this.newPosition,
                    requirement : 1
                })
            }
            this.newPosition = ""

        },

        resetData : function(){
            this.title = ""
            this.artist = ""
            this.content = ""
            this.newPosition = ""
            this.positions = [
                {
                    name: 'Vocal',
                    requirement: 0,
                },
                {
                    name: 'Guitar',
                    requirement: 0,
                },
                {
                    name: 'Bass',
                    requirement: 0,
                },
                {
                    name: 'Drum',
                    requirement: 0,
                },
                {
                    name: 'Keyboard',
                    requirement: 0,
                }
            ]
        },

        createSong : function(){
            axios({
                method : "POST",
                url : url,
                headers : setToken(),
                params : {
                    user_id : localStorage.getItem('user'),
                    project_id : this.$route.query.project_id,
                    title : this.title,
                    artist : this.artist,
                    content: this.content,
                    positions : JSON.stringify(this.positions)
                }
            })
            .then((response) => {
                console.log(response)
                // 그냥 연속생성하자
                // 아래에 non-overlapping 알림 띄우고 수 초안에 collapse하게
                // 그리고 값만 비워주자 
                this.resetData()
            }).catch((error) => {
                console.log("Failed to get retreival", error.response);
            });
        },

    },

    mounted() {

    }

    }
</script>


<style scoped>
    .btn-container{
        margin-left: auto!important;
    }
</style>