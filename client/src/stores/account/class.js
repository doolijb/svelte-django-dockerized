import { AuthRequestHandler } from '../../api'
import uri from '../../api/uri'
import { accountStore } from '../index'

class Account {
    constructor () {
        this.userName = null
        this.isAuth = false
        this.passwordSet = true
        this.email = null // Primary email
        this.emails = [] // All attached emails
        this.isStaff = false
        this.status = { value: 0, label: 'Unauthorized' }
        this.social = {
        }
        this.favorites = []
        this.expiredConnections = []
    }

    toggleLike (id) {
        switch (this.favorites.includes(id)) {
        case true:
            this.favorites = this.favorites.filter((oldId) => oldId != id)
            break
        default:
            this.favorites.push(id)
            break
        }
    }

    async get () {
        const response = await new AuthRequestHandler(
            uri.account.get,
            {},
            (response) => {
                // Grab account data
                const account = response.data.account
                // Modify store
                this.userName = account.userName
                this.isAuth = account.isAuth
                this.passwordSet = account.passwordSet
                this.email = account.email
                this.emails = account.emails
                this.isStaff = account.isStaff
                this.status = account.status
                this.social = account.social
                this.favorites = account.favorites
                this.expiredConnections = account.expiredConnections
                accountStore.set(this)
                return response
            }
        ).get()
        return response
    }

    async login (body) {
        const response = await new AuthRequestHandler(
            uri.account.login,
            body
        ).post()
        // authTokenHandler.set(response.data))
        await this.get()
        return response
    }

    async logout () {
        const response = await new AuthRequestHandler(uri.account.logout, {}).post()
        // authTokenHandler.clear()
        await this.get()
        return response
    }

    async register (body) {
        const response = await new AuthRequestHandler(
            uri.account.register,
            body
        ).post()
        // authTokenHandler.set(response.data)
        await this.get()
        return response
    }

    async sendEmailConfirmation (email) {
        const response = await new AuthRequestHandler(
            uri.account.sendEmailConfirmation,
            { email }
        ).post()
        await this.get()
        return response
    }

    async setPrimaryEmail (email) {
        const response = await new AuthRequestHandler(uri.account.email, {
            email
        }).put()
        await this.get()
        return response
    }

    async addEmail (email) {
        const response = await new AuthRequestHandler(uri.account.email, {
            email
        }).post()
        await this.get()
        return response
    }

    async deleteEmail (email) {
        const response = await new AuthRequestHandler(
            uri.account.email,
            { email }
        ).delete()
        await this.get()
        return response
    }

    async changePassword ({ old_password, new_password, new_password2 }) {
        const response = await new AuthRequestHandler(
            uri.account.password.update,
            { old_password, new_password, new_password2 }
        ).put()
        await this.get()
        return response
    }

    async passwordResetEmail ({ email }) {
        const response = await new AuthRequestHandler(
            uri.account.password.reset,
            { email }
        ).post()
        return response
    }

    async passwordResetVerifyToken ({ token }) {
        const response = await new AuthRequestHandler(
            uri.account.password.reset,
            { token }
        ).get()
        return response
    }

    async passwordResetChangePassword ({ token, new_password, new_password2 }) {
        const response = await new AuthRequestHandler(
            uri.account.password.reset,
            { reset_token: token, new_password, new_password2 }
        ).put()
        return response
    }

    async passwordSetMissing ({ new_password, new_password2 }) {
        const response = await new AuthRequestHandler(
            uri.account.password.set,
            { new_password, new_password2 }
        ).post()
        return response
    }

    async socialConnect ({ provider, code }) {
        const response = await new AuthRequestHandler(
            `${uri.account.social_account}${provider}/`,
            { code },
            () => {},
            0
        ).post()
        await this.get()
        return response
    }

    async socialRefresh ({ provider }) {
        const response = await new AuthRequestHandler(
            `${uri.account.social_account}${provider}/`,
            { provider },
            () => {},
            0
        ).patch()
        await this.get()
        return response
    }

    async socialDelete ({ provider }) {
        const response = await new AuthRequestHandler(
            `${uri.account.social_account}${provider}/`
        ).delete()
        await this.get()
        return response
    }
}

export default Account
