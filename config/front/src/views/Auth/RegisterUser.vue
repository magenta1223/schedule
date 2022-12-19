<template>


<v-parallax
    align="center"
    :height="windowHeight"
    :src="require('@/assets/wallpaper.jpg')"
  >
    <div class="d-flex flex-column fill-height justify-center align-center text-white">
        <v-card class="elevation-12 transparent-body" width="60%">
            <v-card-title class="text-white">
                Register Form
            </v-card-title>


            <v-card-text >
                <v-form>
                    <v-text-field
                        v-model="user.username"
                        class = "text-white"
                        name="username"
                        label="Email/ID"
                        type="text"
                    ></v-text-field>
                    <v-text-field
                        v-model="user.password"
                        id="password"
                        class = "text-white"
                        name="password"
                        label="Password"
                        type="password"
                        color = "white"

                    ></v-text-field>
                    <v-text-field
                        v-model="user.name"
                        id="name"
                        class = "text-white"
                        name="name"
                        label="Name"
                        type="text"
                        color = "white"

                    ></v-text-field>
                    <v-card-actions class="text-white">
                        <v-btn @click="register">
                            REGISTER
                        </v-btn>
                    </v-card-actions>

                </v-form>
            </v-card-text>



        </v-card>
    </div>
</v-parallax>




</template>

<script>
import axios from "axios";



let url = "http://127.0.0.1:8000/api/register/";
// let url = "http://13.209.73.227:8000/api/register/";


export default {

    name : "RegisterUser",
    data : () => {
        return {
            user : {
                username: "",
                password : "",
                name : "",
                contact : ""
            },
            windowHeight : window.innerHeight
                 
        };
    },


   methods : {

        register :function() {
            axios({
                method: "POST",
                url: url, 
                data: this.user,
            })
                .then((response) => {
                    response
                    console.log("done")
                    this.$emit('registerSuccess', 'unauth')
                })
                .catch((error) => {
                    console.log("Failed to register", error.response);
                });
            },
   },

  mounted(){
    window.onresize = () => {
      this.windowHeight = window.innerHeight
    }
  },





};
</script>

<style>
#register {
    margin-left : auto ;
    color : white;
}

.transparent-body {
    background: rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(10px);
    /* color : rgb(255,255,255); 기본 배경 및 텍스트 컬러 */
    
    /* color : rgb(0,0,0) */

}
</style>
