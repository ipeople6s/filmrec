export default {
    namespaced: true,
    state: {
        alertVisible: false
    },
    getters: {
        alertVisible: state =>state.alertVisible,
    },
    mutations: {
        changeAlertVisible(state, payload){
            state.alertVisible = payload;
        },
    }
}