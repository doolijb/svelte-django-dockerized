const PROTOCOL = window.location.protocol
export const API_HOST = `${PROTOCOL}//${location.hostname}:8000/rest/v1`
console.log(API_HOST)

export default {
    account: {
    // This still needs to be cleaned up more
        get: `${API_HOST}/accounts/account/`, // Get all account/user data
        login: `${API_HOST}/accounts/user/session/login/`, // POST
        logout: `${API_HOST}/accounts/user/session/logout/`, // POST
        register: `${API_HOST}/accounts/user/register/`, // POST
        social_account: `${API_HOST}/accounts/social_account/`, // Requires <slug:provider>
        email: `${API_HOST}/accounts/email_address/`, // POST, PUT, DELETE: Email address
        sendEmailConfirmation: `${API_HOST}/accounts/email_address/verification/`, // POST: Send email confirmation
        password: {
            set: `${API_HOST}/accounts/user/password/`, // POST: Set missing password
            update: `${API_HOST}/accounts/user/password/`, // PUT: Update password
            reset: `${API_HOST}/accounts/user/password/reset/` // GET, POST, PUT: Reset password
        },
        csrf: `${API_HOST}/accounts/csrf/` // GET: CSRF token
    },
    products: {
        get: `${API_HOST}/products/all/`, // Get all products
        download: {
            get: `${API_HOST}/products/download/` // Get download link
        },
        favorite: {
            post: `${API_HOST}/products/favorite/` // Favorite or unfavorite product
        }
    },
    posts: {
        get: `${API_HOST}/posts/all/` // Get all products
    },
    website: {
        get: `${API_HOST}/website/` // Get website data
    }
}
