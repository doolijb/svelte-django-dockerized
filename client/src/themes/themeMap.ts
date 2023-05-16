interface Theme {
    title: string
    value: string
    enabled: boolean
    notes?: string
}

const themes: Theme[] = []

const themeMap = new Map<string, Theme>()

themes.push({
    title: "Crimson",
    value: "crimson",
    enabled: true
})

themes.push({
    title: "Gold Nouveau",
    value: "gold-nouveau",
    enabled: true
})

themes.push({
    title: "Hamlindigo",
    value: "hamlindigo",
    enabled: true
})

themes.push({
    title: "Modern",
    value: "modern",
    enabled: true
})

themes.push({
    title: "Rocket",
    value: "rocket",
    enabled: true
})

themes.push({
    title: "Sahara",
    value: "sahara",
    enabled: true
})

themes.push({
    title: "Seafoam",
    value: "seafoam",
    enabled: true
})

themes.push({
    title: "Skeleton (Default)",
    value: "skeleton",
    enabled: true,
    notes: "Default theme"
})

themes.push({
    title: "Vintage",
    value: "vintage",
    enabled: false
})

for (const theme of themes) {
    if (theme.enabled) {
        themeMap.set(theme.value, theme)
    }
}

export default themeMap
