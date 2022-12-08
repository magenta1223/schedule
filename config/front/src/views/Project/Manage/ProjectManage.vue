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
            <v-row class="blurred align-center justify-start rounded-xl ma-0">
                <v-col class = "ma-4">
                    <h1 class = "font-weight-medium text-white">
                        MANAGE MODE : {{project.title}}
                    </h1>

                    <v-btn @click="save">
                        SAVE
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

    name : "ProjectManage",
    
    data : () => {
        return {
            // windows
            windowHeight : window.innerHeight,
            windowWidth : window.innerWidth,
            
            // manage
            manage : false,

            // project -> props
            project : {
                id : -1
            },

            //songs -> props
            tab_headers : [
                {text : 'Status', value : 'manage_status'},
                {text : 'Songs', value : 'manage_songs'},
                {text : 'Schedule', value : 'project_schedule'},
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
                this.project = response.data
                this.status = this.project.status

                console.log("here")
                this.$router.replace({
                    name : 'manage_status',
                    query : {
                        project_id : this.project.id
                    }
                })
                console.log("here")

            }).catch((error) => {
                console.log("Failed to get retreival", error.response);
            });
        },


        to : function(destination){
            // console.log(this.$router)
            if (this.project.id > -1) {

                let project_id = this.project.id
                console.log('cex', project_id)

                this.$router.push({
                    name : destination,
                    query : {
                        status : this.status,
                        project_id : project_id
                    }})

            } else{
                let project_id = this.$route.query.project_id
                console.log('default', project_id)

                this.$router.push({
                    name : destination,
                    query : {
                        status : this.status,
                        project_id : project_id
                    }})

            }

        },

        

        save : function(){
            console.log('cx')

            this.selectedSongs.map((boolean, song_index)=> {
                this.songs[song_index].fix = boolean
            })


            axios({
                method : "PATCH",
                url : url + this.project.id + '/',
                headers : setToken(),
                params : {
                    user_id : localStorage.getItem('user'),
                    project_id : this.project.id,
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



    },

    mounted() {
        this.retrieveProject()
        window.onresize = () => {
            this.windowHeight = window.innerHeight
        }
    },

    watch : {
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
#parralax{
    background-image : url('~@/assets/wallpaper.jpg');
    background-size: cover;

}

.posting-container{
    width: 80%;
}



.blurred{
    background: rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(2px);
    width : 100% !important;
    height:  100% !important;
}

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

