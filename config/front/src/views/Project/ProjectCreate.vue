<template>
    <v-container class = "posting-container">

        <v-row>
            <v-col class ="text-h2 text-start active mb-2"> Start Project
            </v-col>
        </v-row>
        <!-- Title -->
        <v-row>
            <v-col> 
                <v-text-field v-model="title" placeholder="Title" name="title" type="text"></v-text-field>
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
                @click="createProject()"
                >
                Create!  
                </v-btn>
            </v-col>
        </v-row>
    </v-container>

</template>

<script>
import axios from "axios";
import setToken from "@/utils/auth.js"

let url = "http://127.0.0.1:8000/api/project/";  // 장고 drf 서버 주소

export default {
    
    name : "ProjectCreate",

    data : () => {
        return {
            title : "",
            content : "",
            update : false,
            }
        },

    components : {
    },
    
    methods: {
        createProject : function(){
            axios({
                method : "POST",
                url : url,
                headers : setToken(),
                params : {
                    user_id : localStorage.getItem('user'),
                    title : this.title,
                    content: this.content
                }
            })
            .then(
                this.$router.push({
                    name : "projects",
                })
            )
        },

        // updateProject : function(){
        //     axios({
        //         method : "PUT",
        //         url : url + this.wrapper_id + '/',
        //         headers : setToken(),
        //         params : {
        //             content_type : "post",
        //             category_id : this.category_id,
        //             user_id : localStorage.getItem('user'),
        //             title : this.title,
        //             content: this.content
        //         }
        //     }).then(
        //         router.push({
        //             name : "post_retrieval",
        //             params : {
        //                 category_id : this.category_id,
        //                 wrapper_id : this.wrapper_id,
        //                 content_type : 'post',
        //             }
        //         })
        //         )
        // },
        

        // createOrUpdate : function(){
        //     if (this.update){
        //         this.updatePost()
        //     } else {
        //         this.createPost()
        //     }
        // },
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