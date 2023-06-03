// eslint-disable-next-line no-undef
module.exports = {
    env: {
        browser: true,
        es2021: true
    },
    extends: [
        "plugin:svelte/prettier",
        "eslint:recommended",
        "plugin:@typescript-eslint/recommended",
        "plugin:storybook/recommended",
    ],
    overrides: [
        {
            files: ["**/*.svelte"],
            parser: "svelte-eslint-parser",
            parserOptions: {
                parser: "@typescript-eslint/parser"
            }
        }
    ],
    parser: "@typescript-eslint/parser",
    parserOptions: {
        ecmaVersion: "latest",
        sourceType: "module"
    },
    plugins: ["@typescript-eslint", "prettier", "import", "eslint-plugin-import", "sort-keys-fix", "sort-exports"],
    rules: {
        "@typescript-eslint/ban-ts-comment": [
            "off",
        ],
        "import/order": ["error", {"groups": ["index", "sibling", "parent", "internal", "external", "builtin", "object", "type"]}],
        indent: ["error", 4],
        "linebreak-style": ["error", "unix"],
        quotes: ["error", "double"],
        semi: ["error", "never"],
        "sort-imports": [
            "warn",
            {
                ignoreCase: true,
                ignoreDeclarationSort: true,
                ignoreMemberSort: false,
                memberSyntaxSortOrder: ["none", "all", "multiple", "single"]
            },
        ],
        "sort-keys-fix/sort-keys-fix": ["warn"],
        // "sort-vars": ["warn"],
        // "sort-exports/sort-exports": ["error", {"sortDir": "asc"}]
        "no-inner-declarations": "off",
    }
}
