export default function (milisec) {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve('')
        }, milisec)
    })
}
