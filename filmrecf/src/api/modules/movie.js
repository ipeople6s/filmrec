export default ({request}) => ({
    MOVIES(data = {}) {
        return request({
            url: "/api/movies",
            method: "GET",
            params: data
        })
    },
    RATING(data = {}) {
        return request({
            url: "/api/rate",
            method: "GET",
            params: data
        })
    },
    SEARCH(data = {}) {
        return request({
            url: "/api/search",
            method: "post",
            data: data
        })
    },
    ALGO(data = {}) {
        return request({
            url: "/api/algo",
            method: "post",
            data: data
        })
    },
})