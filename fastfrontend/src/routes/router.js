import Vue from 'vue';
import VueRouter from 'vue-router';
import Fastview from '../components/Fastview.vue';

Vue.use(VueRouter);

export default new VueRouter({
  mode:'history',
  routes:[
    {
      path:'/',
      name:'Fastview',
      component: Fastview,
    },
  ],
})
