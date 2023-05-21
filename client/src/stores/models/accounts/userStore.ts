import {writable} from "svelte/store"
import type {IUser} from "src/interfaces"

class UserStore {
    objects: any
    currentId: any

    constructor() {
        this.objects = writable<Map<string, IUser>>(new Map())
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
