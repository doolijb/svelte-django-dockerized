import { writable } from 'svelte/store'
import type { User } from 'src/interfaces'

class UserStore {
    objects: any
    currentId: any

    constructor() {
        this.objects = writable<Map<string, User>>(new Map())
    }

    async get(query: any) {
        // TODO: Implement
    }

    async create(data: any) {
        // TODO: Implement
    }
}

const userStore = new UserStore()

export default userStore
