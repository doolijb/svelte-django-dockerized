/**
 * Function that passes html text through xss filtering and returns the safe html text.
 */

import xss from 'xss'

export default function (text) {
    return xss(text, {
        whiteList: {
            ...xss.whiteList
        },
        onIgnoreTagAttr: function (tag, name, value, isWhiteAttr) {
            if (name === 'class' || 'style') {
                // escape its value using built-in escapeAttrValue function
                return name + '="' + xss.escapeAttrValue(value) + '"'
            }
        }
    })
}
