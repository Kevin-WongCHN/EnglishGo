import { createRouter, createWebHistory } from "vue-router";
import About from "@/components/About.vue";
import Checkout from "@/components/Checkout.vue";
import Example from "@/components/Example.vue";
import Index from "@/components/Index.vue";
import Quiz from "@/components/Quiz.vue";
const router = createRouter({
    history: createWebHistory('/EnglishGo/'),
    routes: [
        {
            path: "/index",
            name: "index",
            component: Index,
        },
        {
            path: "/about",
            name: "about",
            component: About,
        },
        {
            path: "/quiz",
            name: "quiz",
            component: Quiz,
        },
        {
            path:"/example",
            name:"example",
            component: Example
        }
    ]
});
// 根路由跳转/index
router.beforeEach((to, from, next) => {
    if (to.path === "/") {
        next("/index");
    } else {
        next();
    }
})
export default router;