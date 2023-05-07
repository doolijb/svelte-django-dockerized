

export default {
  "meta": {},
  "id": "_default",
  "_regex": {},
  "_paramKeys": {},
  "file": {
    "path": "src/routes",
    "dir": "src",
    "base": "routes",
    "ext": "",
    "name": "routes"
  },
  "rootName": "default",
  "routifyDir": import.meta.url,
  "children": [
    {
      "meta": {},
      "id": "_default_404_svelte",
      "_regex": {},
      "_paramKeys": {},
      "name": "404",
      "file": {
        "path": "src/routes/404.svelte",
        "dir": "src/routes",
        "base": "404.svelte",
        "ext": ".svelte",
        "name": "404"
      },
      "asyncModule": () => import('../src/routes/404.svelte'),
      "children": []
    },
    {
      "meta": {},
      "id": "_default_auth",
      "_regex": {},
      "_paramKeys": {},
      "name": "auth",
      "module": false,
      "file": {
        "path": "src/routes/auth",
        "dir": "src/routes",
        "base": "auth",
        "ext": "",
        "name": "auth"
      },
      "children": [
        {
          "meta": {},
          "id": "_default_auth_login_svelte",
          "_regex": {},
          "_paramKeys": {},
          "name": "login",
          "file": {
            "path": "src/routes/auth/login.svelte",
            "dir": "src/routes/auth",
            "base": "login.svelte",
            "ext": ".svelte",
            "name": "login"
          },
          "asyncModule": () => import('../src/routes/auth/login.svelte'),
          "children": []
        },
        {
          "meta": {},
          "id": "_default_auth_logout_svelte",
          "_regex": {},
          "_paramKeys": {},
          "name": "logout",
          "file": {
            "path": "src/routes/auth/logout.svelte",
            "dir": "src/routes/auth",
            "base": "logout.svelte",
            "ext": ".svelte",
            "name": "logout"
          },
          "asyncModule": () => import('../src/routes/auth/logout.svelte'),
          "children": []
        }
      ]
    },
    {
      "meta": {},
      "id": "_default_index_svelte",
      "_regex": {},
      "_paramKeys": {},
      "name": "index",
      "file": {
        "path": "src/routes/index.svelte",
        "dir": "src/routes",
        "base": "index.svelte",
        "ext": ".svelte",
        "name": "index"
      },
      "asyncModule": () => import('../src/routes/index.svelte'),
      "children": []
    },
    {
      "meta": {
        "dynamic": true,
        "dynamicSpread": true
      },
      "_regex": {},
      "_paramKeys": {},
      "name": "[...404]",
      "file": {
        "path": ".routify/components/[...404].svelte",
        "dir": ".routify/components",
        "base": "[...404].svelte",
        "ext": ".svelte",
        "name": "[...404]"
      },
      "asyncModule": () => import('./components/[...404].svelte'),
      "children": []
    }
  ]
}
