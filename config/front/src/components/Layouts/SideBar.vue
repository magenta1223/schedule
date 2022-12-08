<template>
      <v-navigation-drawer
        expand-on-hover
        rail
        permanent
        @mouseover="drawer = !drawer"
        @mouseout="drwaer = !drawer"
      >
        <v-list>
          <v-list-item
            prepend-avatar="https://randomuser.me/api/portraits/women/85.jpg"
            :title="username"
            :subtitle="email"
          ></v-list-item>
        </v-list>

        <v-divider></v-divider>

        <v-list density="compact" nav>
            <v-list-item :prepend-icon="icons.mdiHome" @click="to('projects')" title="Home" value="home"></v-list-item>
            <v-list-item :prepend-icon="icons.mdiCalendar" @click="to('calendar')" title="Calendar" value="calendar"></v-list-item>
            <v-list-item :prepend-icon="icons.mdiLogout" @click="Logout" title="Log Out" value="logout"></v-list-item>

        </v-list>
      </v-navigation-drawer>



    


</template>

<script>
import axios from 'axios';
import setToken from "../../utils/auth.js"

import { mdiAccountMultiple, mdiFolder, mdiStar, mdiCalendar, mdiLogout, mdiHome  } from '@mdi/js';


let url = 'http://localhost:8000/api/user/'


export default {
    data(){
        return {
            windowHeight: window.innerHeight,
            windowWidth : window.innerWidth,
            drawer: true,
            items: [
                { title: 'Home', icon: 'mdi-home-city' },
                { title: 'My Account', icon: 'mdi-account' },
                { title: 'Users', icon: 'mdi-account-group-outline' },
            ],
            mini: false,
            username : "",
            email : "",
            icons : {
                 mdiAccountMultiple, mdiFolder, mdiStar, mdiCalendar, mdiLogout, mdiHome
            }
        }
    },



    methods : {
        parseParams : function(destination){
            return {
                name : destination
            }

        },

        Logout : function() {
            localStorage.removeItem('access_token');
            location.reload();
        },
        to : function(destination){
            this.$router.push({
                name : destination,
            })
        },


    },

    mounted() {

        window.onresize = () => {
            this.windowHeight = window.innerHeight
            this.windowWidth = window.innerWidth
        }


        let user = localStorage.getItem('user')

        axios({
            method : "GET",
            url : url + user,
            headers: setToken(),
            params : {
                user_id : user
            }
        }).then((response) => {
            this.username = response.data.name
            this.email = response.data.username
            
        }).catch((response) => {
            console.log("Failed", response)
        })
    },



}
</script>


<style scoped>

a {
  text-decoration: none;
  color : black!important;;
}
</style>