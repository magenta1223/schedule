<template>
    <v-container
      fluid
      class="d-flex flex-row align-start pa-0 align-stretch"
    >
        <SideBar/>
        <router-view class = "container"></router-view> 
    </v-container>


</template>

<script>
import SideBar from "@/components/Layouts/SideBar.vue"

export default {
  name: 'MainView',

  data: () => ({
    
  }),

    components : {
        SideBar,
    },

}
</script>
