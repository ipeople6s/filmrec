import {v4} from "uuid";
import Cookies from "js-cookie";

const cookies = {};

cookies.set = function (name = "default", value = "", cookieSetting = {}) {
    const defaultSetting = {
        expires: 1
    };

    Object.assign(defaultSetting, cookieSetting);

    Cookies.set(name, value, defaultSetting);
};

cookies.get = function (name = "default") {
    return Cookies.get(name);
};

cookies.getAll = function () {
    return Cookies.get();
};

cookies.remove = function (name = "default") {
    return Cookies.remove(name);
};

export {v4 as uuid, cookies};
