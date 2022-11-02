const arr = [
    { "name": "Linkedin", "url": "http://www.linkedin.com" },
    { "name": "Github", "url": "https://www.github.com" },
    { "name": "Twitter", "url": "http://twitter.com" }
]

const socials = [
    { "url": "https://www.linkedin.com/company/tablecheck/", "icon": "https://simpleicons.org/icons/linkedin.svg" },
    { "url": "https://github.com/tablecheck", "icon": "https://simpleicons.org/icons/github.svg" },
    { "url": "https://twitter.com/tablesolution", "icon": "https://simpleicons.org/icons/twitter.svg" }
]

class LinksTransformer {
    //Using HTMLRewriter to add the links
    constructor(links) {
        this.links = links
    }

    async element(element) {
        for (var i = 0; i < this.links.length; i++) {
            var a = '<a href="' + this.links[i].url + '">' + this.links[i].name + '</a>'
            element.append(a, { html: true });
        }
    }
}

class SocialsTransformer {
    //Using HTMLRewriter to update the social links

    constructor(socials) {
        this.socials = socials
    }

    async element(element) {
        for (var i = 0; i < this.socials.length; i++) {
            var a = '<a href="' + this.socials[i].url + '">' + '<svg> <image width=50px xlink:href="' + this.socials[i].icon + '"></image> </svg> </a>'
            element.append(a, { html: true });
        }
    }
}


class BodyHandler {
    element(element) {
        element.setAttribute("class", "bg-gray-800")
    }
}


/**
 * gatherResponse awaits and returns a response body as a string.
 * Use await gatherResponse(..) in an async function to get the response body
 * @param {Response} response
 */


async function handleGet(request) {
    if (request.url.includes("/links") == false) {
        const init = {
            headers: { 'content-type': 'text/html' },
        }
        const url = 'https://static-links-page.signalnerve.workers.dev'
        const response = await fetch(url, init)

        // Initial links
        const links = new HTMLRewriter().on('div#links', new LinksTransformer(arr))
            .on('div#profile', { element: e => e.removeAttribute('style') })
            .on('img#avatar', { element: e => e.setAttribute('src', 'https://avatars0.githubusercontent.com/u/36186781?s=200&amp;v=4') })
            .on('h1#name', { element: e => e.setInnerContent('TableCheck') })
            .transform(response)

        // Social Links
        const social = new HTMLRewriter().on('div#social', { element: e => e.removeAttribute('style') }).transform(links)
        const final = new HTMLRewriter().on('div#social', new SocialsTransformer(socials))
            .on('title', { element: e => e.setInnerContent('Table Check') })
            .on("body", new BodyHandler())
            .transform(social)

        return final
    } else {
        return new Response(JSON.stringify(arr), {
            headers: { 'content-type': 'JSON' }
        })
    }
}

addEventListener('fetch', event => {
    const { request } = event

    if (request.method === "GET") {
        return event.respondWith(handleGet(request))
    }
})