<template>
    <v-sheet
        class="mx-auto"
        max-width="100%"
    >
        <v-slide-group
        v-model="model"
        class="pa-4"
        >
            <v-slide-group-item>
                <NewProject/>
            </v-slide-group-item>
            <v-slide-group-item
                v-for="project in projects"
                :key="project"
            >
                <ProJect
                    img_src = "https://cdn.vuetifyjs.com/images/cards/docks.jpg"
                    :project_id="project.id" 
                    :title="project.title"
                    subtitle = "subtitle"
                    :desc="project.content"
                />
            </v-slide-group-item>
        </v-slide-group>


    </v-sheet>
</template>


<script>
import axios from 'axios'
import setToken from '@/utils/auth.js'

import ProJect from "@/components/Project/Project.vue"
import NewProject from "@/components/Project/NewProject.vue"


let url = "http://127.0.0.1:8000/api/project/"; 


export default {
    name: 'ProjectList',

    data: () => ({
        model: null,
        projects : []
        
    }),

    components:{
        ProJect,
        NewProject
    },

    mounted(){
        // console.log(localStorage.getItem("user"))
        axios({
            method: "GET",
            url: url, // localhost:8000/user/1 로 delete method
            headers: setToken(),
            params: {
                user_id : localStorage.getItem('user'),
            },
        })
            .then((response) => {
                // console.log(response.data);
                this.projects = response.data
                // console.log("done")

                // js redirect
                // window.location.href = 'http://localhost:8080/';
                // vue
                //this.$router.push({ name : 'home'})

            })
            .catch((error) => {
                console.log("Failed to get song list", error.response);
            });
    }


}
</script>

<style scoped>
    .blurred{
        background: rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(2px);
    }
</style>