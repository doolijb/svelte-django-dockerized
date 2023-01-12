import Account from './class'

// Logged Out
export const exampleAccountDefault = new Account()

// Logged In
export const exampleAccountLoggedIn = new Account()
exampleAccountLoggedIn.isAuth = true
exampleAccountLoggedIn.userName = 'ChariotDev'
exampleAccountLoggedIn.email = 'contact@chariot-dev.com'
exampleAccountLoggedIn.emails = [
    { email: 'contact@chariot-dev.com', confirmed: true },
    { email: 'example2@chariot-dev.com', confirmed: false },
    { email: 'example3@chariot-dev.com', confirmed: true },
    { email: 'example5@chariot-dev.com', confirmed: true }
]

export const exampleAccountLoggedInPatreon = new Account()
exampleAccountLoggedInPatreon.isAuth = true
exampleAccountLoggedInPatreon.userName = 'ChariotDev'
exampleAccountLoggedInPatreon.email = 'contact@chariot-dev.com'
exampleAccountLoggedIn.emails = [
    { email: 'contact@chariot-dev.com', confirmed: true },
    { email: 'example2@chariot-dev.com', confirmed: false },
    { email: 'example3@chariot-dev.com', confirmed: true },
    { email: 'example5@chariot-dev.com', confirmed: true }
]
exampleAccountLoggedIn.favoriteList = [2, 5, 7]

exampleAccountLoggedInPatreon.social.patreon.UID = 123456789
exampleAccountLoggedInPatreon.social.patreon.name = 'Example'
exampleAccountLoggedInPatreon.social.patreon.email = 'contact@chariot-dev.com'
exampleAccountLoggedInPatreon.social.patreon.tiers = [1]
exampleAccountLoggedInPatreon.favoriteList = [2, 5, 7]

export const exampleAccountLoggedOut = new Account()
