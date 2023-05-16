import {writable} from "svelte/store"
import type {EmailAddress} from "src/interfaces"

class EmailStore {
    objects: any
    currentId: any

    constructor() {
        this.objects = writable<Map<string, EmailAddress>>(new Map())
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
