import { writable } from 'svelte/store'
import ProductModal from './productModal/class'
import Website from './website/class'
import Products from './products/class'
import Posts from './posts/class'
import Account from './account/class'
import Search from './search/class'
import Api from './api/class'

export const accountStore = writable(new Account())
export const productsStore = writable(new Products())
export const postsStore = writable(new Posts())
export const productModalStore = writable(new ProductModal())
export const websiteStore = writable(new Website())
export const searchStore = writable(new Search())
export const apiStore = writable(new Api())
