import router from "@/router/index";
import {cookies} from "./utils";

router.beforeEach(async (to, from, next) => {
    next();
})