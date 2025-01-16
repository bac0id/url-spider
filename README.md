# URL Spider

A crawler to get all URLs in a web page in distance, and output as plain text.

| | |
|-|-|
| English | [简体中文](README-zh_cn.md) |

## Overview

The crawler takes 2 main parameters: the initial URL `url_start` and the maximum distance `max_distance`. The distance refers to the number of clicks required to travel from the initial URL to another URL (you often click on web pages, don't you?).

The main structure of the crawler's algorithm is a breadth-first search (BFS), and the core process is to select a URL from a list of known URLs, followed by obtaining the values of the href attributes of all the `<a>` tags on its web page (a.k.a. the outlinks), and then converting these outlinks to absolute paths and adding them to the list of known URLs.

The results of the crawler come from the filtered queue. The results are written to a file.

The crawler supports both single crawling and continuous crawling. Continuous crawling can cope with the changes in the web page at any time.

### Example

#### Example Website

Imagine you are visiting the website of a pizza company. The protocol "http://" in URLs are ignored. 

```
pizza.com/                             # 2 links at homepage: Order and Job
| pizza.com/order.htm                  # 1 link to download the menu and 2 links to order pizza
  | pizza.com/pizza/menu.pdf
  | pizza.com/order.htm?pizza_id=1
    | pizza.com/cashier.htm
  | pizza.com/order.htm?pizza_id=2
    | pizza.com/cashier.htm
| jobs.pizza.com
  | jobs.pizza.com/city                # link to find jobs in different cities
    | jobs.pizza.com/city/london
    | jobs.pizza.com/city/washington
  | jobs.pizza.com/search.htm?title=manager
  | javascript.void(0);                # link for script
  | mailto:jobs@pizza.com              # link for email
```

#### Example Input

```
   url_start: http://pizza.com
max_distance: 2
```

#### Example Output

Visualized list of recorded URLs ( `*` = recorded )

```
* pizza.com/
* | pizza.com/order.htm
*   | pizza.com/pizza/menu.pdf
*   | pizza.com/order.htm?pizza_id=1
      | pizza.com/cashier.htm           (distance=3 exceed max_distance=2)
*   | pizza.com/order.htm?pizza_id=2
      | pizza.com/cashier.htm           (distance=3 exceed max_distance=2)
* | jobs.pizza.com/
*   | jobs.pizza.com/city
      | jobs.pizza.com/city/london      (distance=3 exceed max_distance=2)
      | jobs.pizza.com/city/washington  (distance=3 exceed max_distance=2)
    | javascript.void(0);               (not http url)
    | mailto:resume@pizza.com           (not http url)
```

Output as plain text:

```
http://pizza.com/
http://pizza.com/order.htm
http://pizza.com/pizza/menu.pdf
http://pizza.com/order.htm?pizza_id=1
http://pizza.com/order.htm?pizza_id=2
http://jobs.pizza.com/
http://jobs.pizza.com/city
```


## Quick Start

1.  Clone
    
    ```
    git clone https://github.com/bac0id/url-spider.git
    ```

2.  Run

    Get URLs at `ttps://example.com`, set `max_distance` to 2, output to file `urls.txt`, mode of crawling to `0` (one time crawling).
    
    ```
    python main.py https://example.com -d 2 -f urls.txt -m 0
    ```

3.  Check result

    ```
    cat urls.txt
    ```
