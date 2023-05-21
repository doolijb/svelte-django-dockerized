import {writable} from "svelte/store"
import type {IEmailAddress} from "src/interfaces"

class EmailStore {
    objects: any
    currentId: any

    constructor() {
        this.objects = writable<Map<string, IEmailAddress>>(new Map())
    }

    async get(query: any) {
        // TODO: Implement
    }

    async create(data: any) {
        // TODO: Implement
    }
}

const emailStore = new EmailStore()

export default emailStore
