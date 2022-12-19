<template>
    <v-container>
        <!-- 헤더 -->
        <v-row class ="mb-4">
            <v-col cols="4">
                <v-select
                    v-model="activeView"
                    :items="activeViewOptions"
                    item-title="name"
                    item-value="name"
                    label="View"
                    density="compact"
                ></v-select>
            </v-col>
            <v-col cols="4">
                <v-btn
                    class ="mr-1"
                    @click="$refs.vuecal.previous()"
                    :icon="icons.mdiArrowLeft"
                    size="small"
                >
                </v-btn>
                <v-btn
                    
                    @click="$refs.vuecal.next()"
                    :icon="icons.mdiArrowRight"
                    size="small"
                >
                </v-btn>
            </v-col>
            <v-col>
                {{selectedDate}}
            </v-col>
            <v-col cols="2">
                <v-btn @click="modal"> SEARCH </v-btn>
            </v-col>
        </v-row>
        
        <!-- 캘린더 -->
        <v-row>
            <v-item-group multiple>
                <VueCal
                    ref="vuecal"
                    v-model:selected-date="selectedDate"
                    v-model:active-view="activeView"
                    hide-view-selector
                    hide-title-bar
                    :events="events"
                    :disable-views="disable_views"
                    :time-from="time_from"
                    :time-to="time_to"
                    :time-step="time_step"
                    :events-on-month-view="eomv"
                    :on-event-click="onEventClick"
                    @cell-click="onCellClick"
                >
                    <template #weekday-heading={heading}>
                        <div :style="wdHeaderStyle(heading)">
                            {{wdHeaderText(heading)}}
                        </div>
                    </template>
                    
                    <template #cell-content="{ cell, view, events, goNarrower }" >
                        <div class="vuecal__flex vuecal__cell-content custom-cell" @click="onCellClick(cell)">
                            <!-- <v-row class ="ma-2">
                                {{ cell.content }}
                            </v-row> -->
                            <v-item v-slot="{ isSelected, toggle }">
                                <v-card
                                :color="isSelected ? 'primary' : ''"
                                class="d-flex align-center rounded-0 elevation-0"
                                dark
                                @click="[onCellClick(isSelected, cell), toggle()]"
                                height="100%"
                                width="100%"
                                >
                                <v-card-text class="text-center">
                                    {{cell.content}}
                                    <!-- {{ isSelected ? 'Selected' : 'Click Me!' }} -->
                                </v-card-text>
                                </v-card>
                            </v-item>

                        </div>
                        <span class="vuecal__cell-date" :class="view.id" v-if="view.id === 'day'" @click="goNarrower">
                        {{ cell.content }}
                        </span>
                        <span class="vuecal__cell-events-count" v-if="view.id === 'month' && events.length">{{ events.length }} </span>
                        <span class="vuecal__no-event" v-if="['week', 'day'].includes(view.id) && !events.length">Nothing here 👌</span>
                    </template>
                </VueCal>
            </v-item-group>
        </v-row>
        <!-- 모달 -->
        <v-row>
            <v-dialog
            v-model="openAddMeeting"
            fullscreen
            :scrim="false"
            transition="dialog-bottom-transition"
            >

                <v-card>
                    <!-- 툴바 -->
                    <v-toolbar
                    dark
                    color="primary"
                    >
                        <v-btn
                            :icon="icons.mdiClose"
                            dark
                            @click="openAddMeeting = false"
                        >
                        </v-btn>

                        <v-toolbar-title>
                            Searching best meeting
                        </v-toolbar-title>
                    </v-toolbar>

                    <!-- 참여 가능 인원 받아오기 -->
                    <v-container v-if="dialogView==='condition'">
                        <!-- 시간 constraint -->
                        <div class="text-h3">Time</div>
                        <v-range-slider
                            :min="9"
                            step="1"
                            thumb-label="always"
                            :max="24"
                            v-model="timeRange"
                            strict
                        ></v-range-slider>
                        <!-- 곡 constraint -->
                        <div class="text-h3">Songs</div>

                        <v-chip-group v-model="selectedSongs" multiple >
                            <v-chip v-for="song in project.songs" :key="song" filter>
                                {{song.title}}
                            </v-chip>
                        </v-chip-group>
                        <div class="text-h3">Dates</div>
                        <!-- 클릭 시, 배치 뷰로 바뀌어야 됨 -->
                        <v-card v-for="date in constrainedDates" :key="date" class="ma-0 pa-0" @click="arrangeView(date)" :ripple="true"> 
                            <v-card-title>
                                {{date}}
                            </v-card-title>
                            
                            <v-chip-group class="ma-2">
                                
                                <v-chip v-for="song in getSongs(date)" :key="song">
                                    {{song.title}}
                                </v-chip>
                            </v-chip-group>
                            
                            <v-divider></v-divider>
                        </v-card>

                    </v-container>


                    <v-container v-else-if="dialogView==='arange'">

                        <!-- 드래그 좋은데, drag를 막기가 어려움. 그냥 위아래 버튼 넣어서 하자 -->
                        <!-- <table>
                            <thead>
                            <tr>
                                <th scope="col">Time</th>
                                <th scope="col">Index</th>
                                <th scope="col">Sport</th>
                                <th scope="col">Artist</th>
                            </tr>
                            </thead>
                            <draggable v-model="draggableList" tag="tbody" item-key="song">
                            <template #item="{element}">
                                <tr>
                                    <td scope="row">{{ element.time }}</td>
                                    <td>{{ element.index }}</td>
                                    <td>{{ element.song.title }}</td>
                                    <td>{{ element.song.artist }}</td>
                                </tr>
                            </template>
                            </draggable>
                        </table> -->


                        <EasyDataTable
                            :headers="headers"
                            :items="getAvailableSongs()"
                            table-class-name="customize-table"
                            show-index
                            body-text-direction ="center"
                            header-text-direction = "center"
                            :hide-footer="true"
                            :hide-rows-per-page="true"
                        >
 


                            <template #item-song="{song}">
                                <td>
                                {{song.title}}
                                </td>
                            </template>
                            <template #item-artist="{song}">
                                <td>
                                {{song.artist}}
                                </td>
                            </template>

                        </EasyDataTable>
                        <v-btn @click="createMeeting"> submit </v-btn>
                        
                    </v-container>
                    <!-- 일단 되는 사람 다 불러오고 -->
                    <!-- 시간대, 곡 등을 조건을 걸어본다. 그에 맞춰서 disable되는 곡이나 사람이 생기겠지? -->
                    <!-- 시간대를 조건으로 걸면?  -->

                    <!-- 조건 다 골랐으면 배치를 해야됨. -->
                    <!-- phase 별로 페이지 짜야됨. 페이지 넘기기 -->
                    


                </v-card>
            </v-dialog>

        </v-row>

    </v-container>
</template>

<script>
import axios from "axios"
import VueCal from 'vue-cal'
import 'vue-cal/dist/vuecal.css'
// import Datepicker from '@vuepic/vue-datepicker';
import {mdiArrowLeft, mdiArrowRight, mdiClose} from "@mdi/js"

import setToken from "@/utils/auth.js"

let url = "http://127.0.0.1:8000/api/project/";  // 장고 drf 서버 주소
let meeting_url = "http://127.0.0.1:8000/api/meeting/";  // 장고 drf 서버 주소


export default {
    name: 'YourComponent',

    data : () => {
        return {
            icons : {
                mdiArrowLeft, mdiArrowRight, mdiClose
            },
            
            // calendar header
            selectedDate: null,
            activeView: "month",
            activeViewOptions : ['month', 'week', 'day'],
            
            // views 
            disable_views : ['years', 'year'],
            disable_days : [], // 이거 computed로 설정. 곡 넣을 때 
                    
            // week / day time interval
            time_from : 8 * 60,
            time_to :23 * 60,
            time_step : 30,

            // view events in month
            eomv : 'short',
        
            // header
            weekdayHeadings : {
                Sunday : {
                    short : 'Sun',
                    color : 'red'
                },
                Monday : {
                    short : 'Mon',
                    color : 'black'
                },
                Tuesday : {
                    short : 'Tue',
                    color : 'black'
                },
                Wednesday : {
                    short : 'Wed',
                    color : 'black'
                },
                Thursday : {
                    short : 'Thu',
                    color : 'black'
                },
                Friday : {
                    short : 'Fri',
                    color : 'black'
                },
                Saturday : {
                    short : 'Sat',
                    color : 'blue'
                },

            },

            events: [
                {
                    id : 1,
                    author : 1,
                    start: '2022-11-26 14:00',
                    end: '2022-11-26 17:30',
                    title: 'Boring event',
                    content: 'CEX',
                    // split : 1
                },
                {
                start: '2022-11-26 12:00',
                end: '2022-11-26 14:00',
                title: '합주',
                class: 'meeting',
                background: true,
                // split : 2
                },
            ],

            // add events
            openAdd : false,
            newDate : [
                new Date(), 
                new Date()
            ],
            newEvent : {
                title : "",
                content : ""
            },

            // retrieve events
            openRetrieve : false,

            selectedNewDates : new Set(),
            openAddMeeting : false,

            timeRange : [12, 22],
            selectedSongs : [],

            dialogView : 'condition',
            sph : 3, // songs per hour,
            selectedDateSchedule : "",
            schedule : [],

            headers : [
                {text : 'Time', value : 'start'},
                {text : 'Title', value : 'song'},
                {text : 'Artist', value : 'artist'},
            ],

            users : []

        }
    },

    components: {
        VueCal,
        // Datepicker
    },

    methods : {
        wdHeaderStyle : function(heading){
            if (heading.label === ''){
                return ''
            } else {
                return 'color:' + this.weekdayHeadings[heading.label].color
            }
        },
        wdHeaderText : function(heading){
            if (heading.label === ''){
                return ''
            } else {
                return this.weekdayHeadings[heading.label].short
            }
        },

        onEventClick: function(event){
            event;
            console.log('eventclick')
        },

        onCellClick : function(isSelected, event){
            event;
            // isSelected === true : 이제 선택 안함
            // isSelected === false : 이제 선택 함
            // selected events에서 제거할지 말지 ? 
            if (typeof(isSelected) === 'boolean'){
                if (!isSelected){
                    console.log(event.startDate)
                    this.selectedNewDates.add(String(event.startDate))
                } else {
                    this.selectedNewDates.delete(String(event.startDate))
                }
            } 

            // console.log('----------------------------')
            // console.log(isSelected, this.selectedNewDates)
            // console.log('----------------------------')

        },

        retrieveProject : function(){
            axios({
                method : "GET",
                url : url + this.$route.query.project_id + '/',
                headers : setToken(),
                params : {
                    user_id : localStorage.getItem('user'),
                }
            }).then((response) => {
                this.project = response.data // project만 가져오자. songs는 songs list에서 가져오고 
                this.project.songs.map((song, index) => {
                    song.index = index
                    return this.parsePlayer(song)
                })
            }).catch((error) => {
                console.log("Failed to get retreival", error.response);
            });
        },

        parsePlayer : function(song){
            song.players.map((player) => {
                if (player.fixed){
                    //song[player.position] = player 
                    song[player.player.position] = player.player.user.name 
                }
            })
            return song
        },


        modal : function(){
            
            this.openAddMeeting = true
            this.dialogView = 'condition'
            console.log(this.selectedNewDates)
            this.getSongs()

        },

        
        // 1. 전체 사용자에 대해 날짜별, 시간대별로 가능한 곡을 전부 뽑는다. 
        // 2. 리스팅

        // 이걸 날짜별로 나누고 싶어.
        // 1. 전체 사용자에 대해 일정 contraint를 고려해, 날짜별로 가능한 곡을 전부 뽑아본다
        // 2. 여기에 추가적으로 합주시간 범위를 지정. global contraint
        // 3. 곡에 대한 constraint : 
        // 1번과 조건이 역임.
        // 어떤 곡에 대해, 현재 선택된 날짜들로 가봄
        // 날짜와 곡이 동시에 주어진 상황. 되냐?
        // 

        getSongs : function(date){
            // 일단은 하루별로 가능한 곡을 뽑아봄. 
            let availableSongs = Array()
            
                // 탐색의 범위를 줄이기 위해. 일부라도 가능하면.. 
            
            for (let j in this.project.songs){
                let song = this.project.songs[j]
                
                for (let t = this.timeRange[0]; t < this.timeRange[1]; t++) {
                    console.log(song.title, date, t, this.isAvailableAt(song, date, t))
                    if(this.isAvailableAt(song, date, t)){
                        availableSongs.push(song)
                        break
                    }
                }
            }


                // 2) song. 루프 돌기전에 그 곡들을 먼저 체크. 하나라도 안되면 그날은 안되는 날.

                
            
            return availableSongs

        },

        isAvailableAt(song, date, time){
            let songStart = new Date(date)
            let songEnd = new Date(date)
            songStart.setHours(time)
            songEnd.setHours(time + 1)


            for (let i in song.players){
                let songplayer = song.players[i]

                if (!songplayer.fixed){
                    // fixed player 만 고려 
                    continue
                }

                let events = songplayer.player.user.events
                for (let j in events){
                    let event = events[j]
                    let eventStart = new Date(event.start)
                    let eventEnd = new Date(event.end)
                    if (event.allDay){
                        eventEnd.setHours(23, 59, 59)
                        if (songStart <= eventEnd && songEnd > eventStart){
                            return false
                        }
                    } else {
                        if (songStart <= eventEnd && songEnd > eventStart){
                            return false
                        }    
                    }
                }
            }

            return true

        }, 

        priorityCompare : function(a, b){
            if (a.priority < b.priority){
                return -1
            } else if (a.priority > b.priority){
                return 1
            } else {
                return 0
            }
        },

        priorityFunction : function(start, H, availableSongs, songs, date){


           // priority는 구간별로 구해야 함./ 
            for (let j in songs){
                let song = songs[j]
                for (let t = start; t < this.timeRange[1] - H; t++) {
                    if(this.isAvailableAt(song, date, t)){
                        song.priority ++; 
                        console.log(song)
                        break
                    }
                }
            }


            songs.sort(this.priorityCompare)
            let maxPriority = songs[songs.length - 1].priority

            // step 2. s_t ~ s_{t+n}까지 순회하면서,
            // priority가 작은 순으로 곡을 투입
            // let table = Array.from(Array(this.timeRange[1] - this.timeRange[0]), () => new Array(songs.length))
            let schedule = Array()
            let users = new Set()
            let table = new Array(H).fill(0).map(() => new Array(songs.length).fill(0));

            for (let t = start; t < start + H; t++) {

                // console.log("now T : ", t )
                // console.log("Range : ", Math.max(t - H - start, 0), t+H - start, H)
                
                let song_at_t = availableSongs[t]
                
                song_at_t.sort(this.priorityCompare)

                let selected = song_at_t.splice(0, this.sph)

                
                selected.map((song, i) => {
                    song.priority = song.priority + maxPriority
                    
                    for (let t_ = Math.max(t - H - start, 0); t_ < t+H - start; t_ ++ ){
                        // console.log(t_, song, table[t_])
                        table[t_][song.index] = 1
                    } 
                    song.players.map((player) => {
                        // users.push(player.player.user.id)
                        users.add(player.player.user.id)
                    })

                    let startTime = new Date(date)
                    let endTime = new Date(date)

                    startTime.setHours(t, this.sph * i)
                    endTime.setHours(t, this.sph * (i+1))

                    schedule.push({
                        start : startTime,
                        end : endTime,
                        song : song
                    })
                })
                
                // schedule.push({
                //     time : t,
                //     songs : selected
                // })
                
                // schedule[t] = song_at_t.splice(0, this.sph)
                // - step 2-4) 추가한 곡의 priority에 max(priority) 만큼을 추가. 
                // schedule[t].map((song) => {
                //     song.priority = song.priority + maxPriority
                    
                //     for (let t_ = Math.max(t - H - start, 0); t_ < t+H - start; t_ ++ ){
                //         console.log(t_, song, table[t_])
                //         table[t_][song.index] = 1
                //     } 
                //     return song
                // })

            }
            // 그냥 여기서 unique한 것만 세면 됨. 
            // 그게 가장 큰걸 선택해서 박으면 됨 

            // - step 3. 이제 t~t+n 시점 까지 배치된 unique한 곡의 개수를 센다. 이게 가장 큰 시간대로 정하면 됨. 
            // 일일히 다 셀 필요가 없다. DP
            // 시간별로 순회하면서, 곡-시간 테이블을 채운다
            // s가 t에서 가능할 때, t-H ~ t+H 까지 전부 채움. 


            let result = table.map((counts) => {

                return counts.reduce((a, b) => a+b, 0)

            }).reduce((a, b) => a+b, 0)


            return [result, schedule, users]

        },

        getAvailableSongs : function(){

            let date = this.selectedDateSchedule
            
            // 탐색의 범위를 줄이기 위해. 일부라도 가능하면.. 
            
            // constrained optimization 

            // given : date, H, room, n_s
            // - date : user의 선택
            // - H    : default는 전곡. 한 시간 당 곡 수를 선택하면 자동으로 결정.
            //     ex ) 전체 15곡에 한시간 당 3곡이면 H=5시간
            // - room : 방 갯수
            //     ex ) 전체 20곡에 방 room=2개, 한 시간당 3곡이면 H=4시간씩 
            // - n_s  : 한 시간 당 진행할 곡의 수. 

            // max 연속된 n시간안에 가능한 합주곡
            // subject to 참여 인원의 스케쥴을 모두 만족
            
            // dual problem
            
            // min 참여인원의 스케쥴을 침해
            // max 연속된 n시간안에 가능한 합주곡 

            // 1. date에서 참여 인원의 스케쥴 침해 최소화 : Done ! 
            // - 모든 스케쥴을 체크, 가능한 곡들을 뽑음
            // - 안와도 되는 사람이 있는지 확인 (optional)

            // 2. 그러면서 연속된 n시간안에 가능한 합주곡 최대화
            
            // 아래는 t ~ t+n 사이에 최적 배치로직
            // - step 1. s_t ~ s_{t+n} 를 count함. 각 곡 별로 가능한 횟수가 나오고, 이게 priority가 된다. 
            // - step 2. s_t ~ s_{t+n}까지 순회하면서,
            //     - step 2-1) s_t의 priority를 체크.
            //     - step 2-2) s_t 중 priority가 작은 순서대로 곡을 투입 
            //     - step 2-3) 나머지 곡 중, 사람이 겹치지 않는 곡들을 추가. 역시 priority 순으로 모든 방을 채운다. 만약 채울 수 없다면, 비워둠.
            //     - step 2-4) 추가한 곡의 priority에 max(priority) 만큼을 추가. 
            // - step 3. 이제 t~t+n 시점 까지 배치된 unique한 곡의 개수를 센다. 이게 가장 큰 시간대로 정하면 됨. 

            
            // 3. 그리고 뭐.. 시간 안에서 변경 정도가 추천사항 ? 

            let songs = this.project.songs

            // console.log(songs)
            songs = songs.map((song) => {
                song.priority = 0
                return song
            })
            
            let availableSongs = {}
            for (let t = this.timeRange[0]; t < this.timeRange[1]; t++){
                availableSongs[t] = Array()
            }
            
            // step 1. s_t ~ s_{t+n} 를 count함. 각 곡 별로 가능한 횟수가 나오고, 이게 priority가 된다. : Done
            let songsCount = 0 /* eslint-disable */
            
            for (let j in songs){
                let song = songs[j]
                let counted = false
                for (let t = this.timeRange[0]; t < this.timeRange[1]; t++) {
                    if(this.isAvailableAt(song, date, t)){
                        availableSongs[t].push(song)
                        if (!counted){
                            songsCount ++;
                            counted = true
                        }
                    }
                }
            }
            
            // get hours required to complete all available songs
            let H = parseInt(songsCount / this.sph) 
            let remainder = songsCount % this.sph
            if (remainder !== 0){
                H ++;
            }
            

            // priority는 구간별로 구해야 함./ 
                        
            // 몇시부터 시작하는게 최적인지 나와버림.
            let maxS = -1

            let meeting = {
                schedules : "",
                participants : "",
                title : "test title",
                content : "test content",
                start : "",
                end : "",
            }

            for (let startHour = this.timeRange[0]; startHour < this.timeRange[1] - H; startHour ++){
                let result= this.priorityFunction(startHour, H, availableSongs, songs, date)
                if (result[0] > maxS){
                    let start = new Date(date)
                    let end = new Date(date)
                    
                    start.setHours(startHour)
                    end.setHours(startHour + H)

                    maxS = result[0]
                    meeting.schedules = result[1]
                    meeting.participants =  Array.from(result[2])
                    
                    
                    meeting.start =  start
                    meeting.end = end

                }
            }



            // 이제 optimal T에서 schedule을 구하면 됨. priority funcitno에서 받아오자

            this.meeting = meeting 

            return meeting.schedules
            
        },



        getAvailableDays : function(constraintSongs){
            // 이 곡을 꼭 해야돼
            // 그르면 날짜별로 그 곡이 가능한지 체크를 한다.
            // 되는 날짜를 반환
            constraintSongs;

            this.selectedNewDates.map((date) => {
                date;

            })

            let availableDays = Array()
            return availableDays

        },

        arrangeView : function(date){
            console.log(date)
            this.dialogView = 'arange'
            this.selectedDateSchedule = date
        
        },

        log : function(input){
            console.log(input)
        },

        createMeeting : function(){
            this.schedule
            axios({
                method : "POST",
                url : meeting_url,
                headers : setToken(),
                params : {
                    user_id : localStorage.getItem('user'),
                    project_id : this.$route.query.project_id ,
                    // schedule : JSON.stringify(this.meeting.schedules),
                    // participants : JSON.stringify(this.meeting.participants),
                    meeting : JSON.stringify(this.meeting),
                    action : "meeting"
                }
            }).then((response) => {
                console.log(response)
                
            }).catch((error) => {
                console.log("Failed to get retreival", error.response);
            });


        }
    },

    mounted() {
        this.retrieveProject()
    },

    computed : {
        constrainedDates() {
            if (this.selectedSongs.length === 0){
                return this.selectedNewDates
            } else{


                let dates = new Set();
                
                for (let date of this.selectedNewDates){
                    for (let j in this.selectedSongs){
                        let song = this.project.songs[this.selectedSongs[j]]
                        for (let t = this.timeRange[0]; t < this.timeRange[1]; t++) {
                            if(this.isAvailableAt(song, date, t)){
                                dates.add(date)
                            }
                        }
                    }
                }
                console.log(dates)

                return dates
            }
            
        }
    }

    // watch : {
    //     selectedSongs : {
    //         handler : function(newVal, oldVal){
    //             oldVal; newVal;
    //             console.log(newVal)
    //         },

    //         intermediate : true,
    //         deep : true
    //     }
    // }

}
</script>


<style>
.v-dialog .v-overlay__content{
    flex-direction : row;
    justify-content : center
}

.vuecal--month-view .vuecal__cell {height: 100px;}

.vuecal--month-view .vuecal__cell-content {
  justify-content: flex-start;
  height: 100%;
  align-items: flex-end;
}

.vuecal--month-view .vuecal__cell-date {padding: 4px;}
.vuecal--month-view .vuecal__no-event {display: none;}
.vuecal--week-view .vuecal__no-event {display: none;}

.vuecal__event.P {
  background: rgb(255, 98, 98);
  display: flex;
  justify-content: center;
  align-items: center;
}

.vuecal__flex[grow]{
    flex:none
}



.vuecal__flex .vuecal__cell-content .custom-cell{
    align-items: center;
    justify-content: center;

}

</style>

