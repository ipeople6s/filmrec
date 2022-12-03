import axios from "axios";
import {assign} from "lodash";
import router from "@/router";
import {cookies} from "./utils";
import {Notification} from 'element-ui';
import store from '@/store/index';

function createService() {

    const service = axios.create({
        baseURL: "http://localhost:8848/",
        timeout: 1000 * 60 * 2,
    });

    service.interceptors.request.use(
        config => {
            config.headers.token = cookies.get("token") || "";
            return config;
        },
        error => {
            console.log(error);
            return Promise.reject(error);
        }
    );

    service.interceptors.response.use(
        response => {

            const dataAxios = response.data;
            console.log(dataAxios);
            const {status, message} = dataAxios;
            if (status === undefined) {
                return dataAxios;
            }
            else {
                switch (status) {
                    case 200:
                        return dataAxios.data;
                    case 401:
                        router.push("/");
                        return Promise.reject({
                            status,
                            message
                        });
                    case 405:
                        store.commit("user/changeAlertVisible", true);
                        router.push("/");
                        return Promise.reject({
                            status,
                            message
                        });
                    default:
                        Notification.error({
                            title: "error",
                            message: message
                        });
                        return Promise.reject({
                            status,
                            message
                        });
                }
            }
        },
        error => {
            const status = error.response.status;
            switch (status) {

                case 401:
                    error.message = "Sign up again";
                    break;
                case 404:
                    error.message = "Request url error";
                    break;
                case 500:
                    error.message = "Error";
                    break;
                default:
                    error.message = "Error";
                    break;
            }

            console.error(error);
            
            this.$notify({
                type: "error",
                title: 'Operation failed',
                message: error.message,
            });

            return Promise.reject(error);
        }
    );

    return service;
}

function createRequestsFunction(service) {
    return function (config) {
        const defalutConfig = {
            timeout: 5000 * 20
        };
        return service(assign({}, config, defalutConfig));
    }
}

export const service = createService();
export const request = createRequestsFunction(service);