<template>
    <v-app>
        <v-main v-if="status==='auth'">
            <MainView/>
        </v-main>
        <v-main v-else-if="status==='unauth'">
            <LogIn
            @register="register"
            />
        </v-main>
        <v-main v-else>
            <RegisterUser
            @registerSuccess="registerSuccess"
            />
        </v-main>
    </v-app>
</template>

<script>
import MainView from '@/views/Main.vue'
import LogIn from '@/views/Auth/LogIn.vue'
import RegisterUser from '@/views/Auth/RegisterUser.vue'

// import axios from "axios";

export default {
  name: 'App',

    data: () => ({
        status : "unauth"
    }),
    created : function(){
        // 로컬스토리지에 jwt 이 존재하는지에 따라 로그인 여부 판단하기
        const token = localStorage.getItem('access_token')
        
        // 이미 로그인한 상태. 
        if (localStorage.getItem("access_token")){
            const expired = (JSON.parse(atob(localStorage.getItem("access_token").split('.')[1]))).exp
            // 토큰만료 시 로그아웃 
            if (expired >= Date.now()/1000){
                this.status = "auth"
                this.$router.push({"name" : "projects"})
            } else {
                this.status = "unauth"
            }
        // 최초 로그인. token이 
        }
        token
        

    },


    components: {
        MainView,
        LogIn,
        RegisterUser
    },

    methods : {
        register : function(status){
            this.status = status
        },
        registerSuccess : function(status){
            this.status = status
        }
    }


}
</script>
