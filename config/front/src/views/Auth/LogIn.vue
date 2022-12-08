<template>
<v-parallax
    align="center"
    :height="windowHeight"
    :src="require('@/assets/wallpaper.jpg')"
  >
    <div class="d-flex flex-column fill-height justify-center align-center text-white">
        <v-card class="elevation-12 transparent-body" width="50%">
            <!-- title -->


            <!-- body -->
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
                </v-form>
            </v-card-text>

            <v-card-actions>
                <v-spacer></v-spacer>
                <v-spacer></v-spacer>
                <v-btn color="white" @click="Login">Sign In</v-btn>
                <v-spacer></v-spacer>
                <a id = "register" class="ma-4" @click="Register" href="#"> or Register </a>
                <v-spacer></v-spacer>
                <v-spacer></v-spacer>
            </v-card-actions>
        </v-card>
    </div>
</v-parallax>


</template>

<script>
import axios from "axios";

let url = "http://127.0.0.1:8000/api/login/";

export default {
    data : () => {
        return {
            user : {
                username: "",
                password : "",
            },
            windowHeight : window.innerHeight
                 
        };
    },


   methods : {
       Login :function() {
        console.log(this.user)
            axios({
                method: "POST",
                url: url, // localhost:8000/user/1 로 delete method
                data: this.user,
            })
                .then((response) => {
                    console.log(response.data);
                    localStorage.setItem("authdata", response.data)
                    localStorage.setItem('access_token', response.data.access_token);
                    localStorage.setItem('refresh_token', response.data.refresh_token);
                    localStorage.setItem('user', response.data.user.id);
                    console.log("done")




                    // js redirect
                    // window.location.href = 'http://localhost:8080/';
                    
                    // vue
                    //this.$router.push({ name : 'home'})
                    console.log(this.$router)
                    this.$router.go(this.$router.currentRoute);
                })
                .catch((error) => {
                    console.log("Failed to get userList", error.response);
                });
        },
    Register :function() {
        // this.$router.push({ name : 'register'})
        this.$emit("register", "register")

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
    background: rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(10px);
    /* color : rgb(255,255,255); 기본 배경 및 텍스트 컬러 */
    
    /* color : rgb(0,0,0) */

}
</style>
