import { createRouter, createWebHistory } from 'vue-router'
//import HomeView from '../views/HomeView.vue'

// Main
import MainView from "@/views/Main.vue"

// Auth
import LogIn from "@/views/Auth/LogIn.vue"
import RegisterUser from "@/views/Auth/RegisterUser.vue"

// projects
import ProjectList from "@/views/Project/ProjectList.vue"
import ProjectCreate from "@/views/Project/ProjectCreate.vue"
import ProjectRetrieve from "@/views/Project/ProjectRetrieve.vue"

// Manage
import ProjectManage from "@/views/Project/Manage/ProjectManage.vue"
import ManageSongs from "@/views/Project/Manage/ManageSongs.vue"
import ManageStatus from "@/views/Project/Manage/ManageStatus.vue"
import ManageSchedule from "@/views/Project/Manage/ManageSchedule.vue"


// song
import SongCreate from "@/views/Song/SongCreate.vue"
import SongList from "@/views/Song/SongList.vue"
import SongFixedList from "@/views/Song/SongFixedList.vue"

// calendar
import CalendarView from "@/views/Event/Calendar.vue"



const routes = [
    // MAIN
    {
        path: '/',
        name: 'home',
        component: MainView
    },

    // AUTH
    {
        path: '/register',
        name: 'register',
        component: RegisterUser
    },
    {
        path: '/login',
        name: 'login',
        component: LogIn
    },

    // PROJECTS

    // List
    {
        path: '/projects',
        name: 'projects',
        component: ProjectList
    },

    // Create
    {
        path: '/project_create',
        name: 'project_create',
        component: ProjectCreate
    },

    // Retreive
    {
        path: '/projects/',
        name: 'project_retreive',
        component: ProjectRetrieve,
        props : true,
        children : [
            // Song Create
            {
                path: '/projects/',
                name: 'song_create',
                component: SongCreate,
            },
            // Song List
            {
                path: '/projects/',
                name: 'song_list',
                component: SongList,
            },
            {
                path: '/projects/',
                name: 'song_fixed_list',
                component: SongFixedList,
            },

        ]
    },

    // Manage
    {
        path: '/manage/',
        name: 'project_manage',
        component: ProjectManage,
        children : [
            {
                path: '/manage/',
                name: 'manage_songs',
                component: ManageSongs,
            },
            {
                path: '/manage/',
                name: 'manage_status',
                component: ManageStatus,
            },
            {
                path: '/manage/',
                name: 'project_schedule',
                component: ManageSchedule,
                props : true
            },

        ]
    },
    
    {
        path: '/calendar/',
        name: 'calendar',
        component: CalendarView,
        props : true
    },

    {
        path: '/calendar/',
        name: 'calendar',
        component: CalendarView,
        props : true
    },

    // SONG
    
    // Create
    // {
    //     path: '/song_create/:project_id',
    //     name: 'song_create',
    //     component: SongCreate,
    //     props : true
    // },
    // List
    // {
    //     path: '/songs/:project_id',
    //     name: 'song_list',
    //     component: SongList,
    //     props : true
    // },






]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
