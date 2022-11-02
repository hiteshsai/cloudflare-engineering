# Problem-2

## Background

This program is an approach to solve the [assignment](https://github.com/tablecheck/tablecheck-2020-systems-engineering-assignment). And also this is an extension of the [cloudflare worker project](https://github.com/tablecheck/tablecheck-2020-general-engineering-assignment).

## Prerequisites

Docker

## Commands to execute this program

### Step - 1

Building the Docker image

```bash
docker build -t problem2 .
```

### Step  - 2

Executing the commands using the built image named `problem2`.

Examples:

- Make an HTTP request to the URL and print the response.

    ```bash

    docker run -it --rm problem2 python main.py --url=worker.saihitesh98.workers.dev

    ```

    Sample output :

    ```bash
    HTTP/1.1 200 OK
    Date: Sun, 08 Nov 2020 07:11:28 GMT
    Content-Type: text/html
    Connection: close
    Set-Cookie: __cfduid=dc9072372ff31f07721f2e675c4becf1d1604819487; expires=Tue, 08-Dec-20 07:11:27 GMT; path=/; domain=.saihitesh98.workers.dev; HttpOnly; SameSite=Lax
    CF-Ray: 5eed7ae7be55ef92-NRT
    cf-request-id: 06484b24d10000ef92f231c000000001
    Expect-CT: max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"
    Report-To: {"endpoints":[{"url":"https:\/\/a.nel.cloudflare.com\/report?s=5S%2FYaOjOmhwDU5O6VBUXolgrtBR4%2BENHA9VnAZ8LLTdoEI308mB1aXP2f8gOTEJWBDmMR5FzW057K8mgCGunVH%2FYGNyNXdZHjgDODFkSNeDbOgfS2LJQggBsNW6YE44%3D"}],"group":"cf-nel","max_age":604800}
    NEL: {"report_to":"cf-nel","max_age":604800}
    Server: cloudflare


    <!DOCTYPE html>
    ...
    </html>
    ```

- Make an HTTP request to the `/links` path and fetches the JSON document.

    ```bash

    docker run -it --rm problem2 python main.py --url=worker.saihitesh98.workers.dev/links

    ```

    Sample output

    ```bash
    [{'name': 'Linkedin', 'url': 'http://www.linkedin.com'}, {'name': 'Github', 'url': 'https://www.github.com'}, {'name': 'Twitter', 'url': 'http://twitter.com'}]
    ```

- Make an HTTP request to the URL and provide the number of requests to your site in the profile argument. Metrics will be displayed in the output.

    ```bash

    docker run -it --rm problem2 python main.py --url=worker.saihitesh98.workers.dev --profile=3

    ```

    Sample output

    ```bash
    The number of requests:  3
    The fastest time:  0.12540686200372875 s
    The slowest time:  0.16650180300348438 s
    The mean time:  0.1413595233364807 s
    The median time:  0.13216990500222892 s
    Error codes are :  []
    Success percentage is :  100.0
    The size in bytes of the smallest response :  927
    The size in bytes of the largest response:  2048
    ```
