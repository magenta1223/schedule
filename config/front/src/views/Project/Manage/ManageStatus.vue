<template>
    <v-container>
        <!-- <v-radio-group v-model="status" inline @change="save"> -->
        <v-radio-group v-model="status" inline>
            <template v-slot:label>
                <strong> Status of Project </strong>
            </template>
            <v-radio
                v-for="option in statusOptions"
                :key="option.value"
                :value="option.value"
                :color="option.color"
            >
                <template v-slot:label>
                    <strong >{{option.name}} </strong>
                </template>
            </v-radio>
        </v-radio-group>
    </v-container>
</template>




<script>
import axios from "axios"
import setToken from "@/utils/auth.js"

let url = "http://127.0.0.1:8000/api/project/";  // 장고 drf 서버 주소

export default {
    name : "ManageStatus" , 


    data : () => {
        return {
                // route : useRoute(),
                // router : useRouter(),
                project_id : -1,
                status : "P",
                statusOptions : [
                    {
                        name : "Prepare",
                        value : "P",
                        color : "orange"
                    },
                    {
                        name : "Ready",
                        value : "R",
                        color : "success"
                    },
                    {
                        name : "OnGoing",
                        value : "O",
                        color : "primary"
                    },
                    {
                        name : "Done",
                        value : "D",
                        color : "error"
                    },                
                ]
        }
    },


    methods : {

        getStatus : function(){
            axios({
                method : "GET",
                url : url + this.$route.query.project_id + '/',
                headers : setToken(),
                params : {
                    user_id : localStorage.getItem('user'),
                }
            }).then((response) => {
                this.status = response.data.status
                this.project_id = response.data.id
            }).catch((error) => {
                console.log("Failed to get status", error.response);
            });
        },

        updateStatus : function(){
             axios({
                method : "PATCH",
                url : url + this.project_id + '/',
                headers : setToken(),
                params : {
                    project_id : this.project_id,
                    status : this.status,
                    action : 'status'
                }
            }).then((response) => {
                console.log(response)
            }).catch((error) => {
                console.log("Failed to update status", error.response);
            });
            
        }
    },

    mounted() {
        this.getStatus()
    },


    watch : {
        status : function(){
            this.updateStatus()
        }
    }




    


    

}
</script>
