# URL Spider

A crawler to get all URLs in a web page in distance, and output as plain text.

| | |
|-|-|
| [English](README.md) | 简体中文 |

# Overview

爬虫需要2个参数：初始URL和最大距离。距离指的是从**初始URL**前往另一个URL所需的点击次数。

爬虫的算法主要结构是宽度优先搜索（BFS）。核心流程是：从已知URL列表中选出一个URL，接着，获取其网页上的所有 `<a>` 标签的 `href` 属性值（也就是链接）。然后，将这些链接转换为绝对路径，并加入已知URL列表。

爬虫的结果来自经过筛选的URL列表。结果将写入文件。

爬虫支持单次爬取和持续爬取。持续爬取可以应对网页的随时变化。

## Example

### Example Website

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

### Example Input

`url_start`: `pizza.com/`

`max_distance`: `2`

### Example Output

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
    | mailto:resume@pizza.com             (not http url)
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


# Quick Start

1.  Clone
    
    ```
    git clone 
    ```

2.  Run

    Get URLs at `ttps://example.com`, set `max_distance` to 2, and output to `urls.txt`.
    
    ```
    python main.py https://example.com -d 2 -f urls.txt
    ```

# License

GNU GPLv3

