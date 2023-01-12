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

function setCookie (name, value, exp_days) {
    const d = new Date()
    d.setTime(d.getTime() + (exp_days * 24 * 60 * 60 * 1000))
    const expires = 'expires=' + d.toGMTString()
    document.cookie =
		name + '=' + value + ';' + expires + ';path=/'
}

function deleteCookie (name) {
    const d = new Date()
    d.setTime(d.getTime() - 60 * 60 * 1000)
    const expires = 'expires=' + d.toGMTString()
    document.cookie = name + '=;' + expires + ';path=/'
}

export default {
    get: () => {
        const access = getCookie('access_token') || null
        const refresh = getCookie('refresh_token') || null
        return { access, refresh }
    },
    set: ({ access, refresh }) => {
        if (access) {
            setCookie('access_token', access, 1)
        }
        if (refresh) {
            setCookie('refresh_token', refresh, 365)
        }
    },
    clear: () => {
        deleteCookie('access_token')
        deleteCookie('refresh_token')
    }
}
