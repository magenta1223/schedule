<template>
    
    <v-container class = "mb-6">
        <!-- 헤더 -->
        <v-container>
        <v-parallax
            id = "parralax"
            class = "rounded-xl"
            :width="windowWidth"
            height="200px"
        >
        <v-row class="blurred rounded-xl ma-0"  justify="space-between" align="center">
                <v-col class = "ma-4">
                    <h1 class = "font-weight-medium text-white">
                        {{project.title}}
                    </h1>
                    <v-btn v-if="manage_mode" @click="to('project_manage')">
                        MANAGE
                    </v-btn>
                </v-col>

        </v-row>
        </v-parallax>
        </v-container>
        <!-- 바디 -->
        <v-tabs
        show-arrows
        v-model="active_tab"
        >

            <v-tab
                v-for="header in tab_headers"
                :key="header.text"
                @click="to(header.value)"
            >
                {{header.text}}

            </v-tab>
        </v-tabs>
        <router-view></router-view>
    </v-container>

</template>



<script>
import axios from "axios";
import setToken from "@/utils/auth.js"
// import { Header, Item } from "vue3-easy-data-table";

let url = "http://127.0.0.1:8000/api/project/";  // 장고 drf 서버 주소



export default {
    
    name : "ProjectRetrieve",

    data : () => {
        return {
            // windows
            windowHeight : window.innerHeight,
            windowWidth : window.innerWidth,
            
            // manage
            manage_mode : false,

            // project
            project : {
                id : 0
            },

            tab_headers : [
            ],
            active_tab : 0
        }
    },

    components : {
    },
    
    methods: {
        retrieveProject : function(){
            axios({
                method : "GET",
                url : url + this.$route.query.project_id + '/',
                headers : setToken(),
                params : {
                    user_id : localStorage.getItem('user'),
                }
            }).then((response) => {
                this.project = response.data // project만 가져오자. songs는 songs list에서 가져오고 
                if (parseInt(localStorage.getItem('user')) === this.project.leader){
                    this.manage_mode = true
                }
                let dest = this.setTabs(this.project.status)

                this.$router.replace({
                    name : dest,
                    query : {
                        project_id : this.$route.query.project_id
                    }
                })
            }).catch((error) => {
                console.log("Failed to get retreival", error.response);
            });
        },

        setTabs : function(project_status){

            if (project_status === 'P'){
                // prepare phase
                this.tab_headers =  [
                    {text : 'Songs', value : 'song_list'},
                    {text : 'Create Song', value : 'song_create'},
                ]
                return 'song_list'

            } else if(project_status === 'R') {
                // ready phase
                this.tab_headers =  [
                    {text : 'Set List', value : 'song_fixed_list'},
                    {text : 'Meeting Schedules', value : 'project_meeting'},
                ] 
                return 'song_fixed_list'

                
            } else if(project_status === 'O') {
                // on-going phase
                this.tab_headers =  [
                    {text : 'Set List', value : 'song_fixed_list'},
                    {text : 'Meeting Schedules', value : 'project_meeting'},
                ]   
                return 'song_fixed_list' 
            } else {
                // ended phase
                this.tab_headers =  [
                    {text : 'Set List', value : 'song_fixed_list'},
                ]         
                return 'song_fixed_list'
            }

        },

        to : function(destination){
            this.$router.push({
                name : destination,
                query : {
                    project_id : this.$route.query.project_id
                }
            })
        },



    },

    mounted() {
        this.retrieveProject()
        // this.to('song_list')
        window.onresize = () => {
            this.windowHeight = window.innerHeight
        }
    },


}
</script>


<style scoped>
#parralax{
    background-image : url('~@/assets/wallpaper.jpg');
    background-size: cover;

}

.posting-container{
    width: 80%;
}

.btn-container{
    margin-left: auto!important;
}

.blurred{
    background: rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(10px);
    width : 100% !important;
    height:  100% !important;
}


</style>

