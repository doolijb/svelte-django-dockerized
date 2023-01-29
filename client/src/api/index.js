import uri from './uri'
import axios from 'axios'

function getCookie (name) {
    const cname = name + '='
    const decodedCookie = decodeURIComponent(document.cookie)
    const ca = decodedCookie.split(';')
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i]
        while (c.charAt(0) == ' ') {
            c = c.substring(1)
        }
        if (c.indexOf(cname) == 0) {
            return c.substring(cname.length, c.length)
        }
    }
    return ''
}

export class AuthRequestHandler {
    constructor (uri, body = {}, then, retries = 2) {
        this.uri = uri
        this.body = body
        this.doThen = then
        this.retries = retries
        this.response = {}
        this.error = {}
        this.headers = {
            // 'Access-Control-Allow-Origin': '*', // Required for CORS support to work
            'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization, Content-Length, X-Requested-With',
            'Content-Type': 'application/json'
        }
    }

    async getCsrfToken () {
        const response = await axios({
            method: 'get',
            url: uri.account.csrf
        })
            .then((response) => {
                return response
            })
            .catch((error) => {
                return error.response
            })
        console.log(response)
        return response
    }

    async get () {
        this.response = await axios({
            method: 'get',
            url: this.uri,
            headers: this.headers,
            params: this.body
        })
            .then((response) => {
                console.log(response)
                return response
            })
            .catch((error) => {
                console.log(error)
                return error.response
            })
        if (this.response.status.toString()[0] == 2) {
            if (this.doThen) {
                this.doThen(this.response)
            }
        }
        return this.response
    }

    async post () {
        const csrfRes = await this.getCsrfToken()

        this.response = await axios
            .post(this.uri, this.body, {
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(function (response) {
                return response
            })
            .catch(function (error) {
                return error.response
            })
        if (this.response.status.toString()[0] == 2) {
            if (this.doThen) {
                this.doThen(this.response)
            }
        }
        return this.response
    }

    async put () {
        const csrfRes = await this.getCsrfToken()

        this.response = await axios
            .put(this.uri, this.body, {
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(function (response) {
                return response
            })
            .catch(function (error) {
                return error.response
            })
        if (this.response.status.toString()[0] == 2) {
            if (this.doThen) {
                this.doThen(this.response)
            }
        }
        return this.response
    }

    async patch () {
        const csrfRes = await this.getCsrfToken()

        this.response = await axios
            .patch(this.uri, this.body, {
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(function (response) {
                return response
            })
            .catch(function (error) {
                return error.response
            })
        if (this.response.status.toString()[0] == 2) {
            if (this.doThen) {
                this.doThen(this.response)
            }
        }
        return this.response
    }

    async delete () {
        const csrfRes = await this.getCsrfToken()

        this.response = await axios
            .delete(this.uri, {
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                data: this.body
            })
            .then(function (response) {
                return response
            })
            .catch(function (error) {
                return error.response
            })
        if (this.response.status.toString()[0] == 2) {
            if (this.doThen) {
                this.doThen(this.response)
            }
        }
        return this.response
    }
}
