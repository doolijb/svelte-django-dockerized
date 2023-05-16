import type {Preview} from "@storybook/svelte"
import {ThemeProvider} from "../src/components/layout"
import themeMap from "../src/themes/themeMap"

const themes = new Array<{value: string; title: string}>()
// loop over theme values
for (const theme of themeMap.values()) {
    themes.push({
        value: theme.value,
        title: theme.title
    })
}

const preview: Preview = {
    parameters: {
        actions: {argTypesRegex: "^on[A-Z].*"},
        controls: {
            matchers: {
                color: /(background|color)$/i,
                date: /Date$/
            }
        }
    },
    decorators: [
        (args, story) => ({
            Component: ThemeProvider,
            props: {
                theme: story.globals.theme,
                darkMode: story.globals.darkMode
            }
        })
    ],

    globalTypes: {
        theme: {
            // Skeleton theme switcher
            name: "Theme",
            description: "Global theme for components",
            defaultValue: "skeleton",
            toolbar: {
                dynamicTitle: true,
                icon: "paintbrush",
                items: themes
            }
        },
        darkMode: {
            name: "Dark Mode",
            description: "Global dark mode for components",
            defaultValue: false,
            toolbar: {
                dynamicTitle: true,
                icon: "circlehollow",
                items: [
                    {value: false, title: "Light", icon: "sun"},
                    {value: true, title: "Dark", icon: "moon"}
                ],
                showName: true
            }
        }
    }
}

export default preview
