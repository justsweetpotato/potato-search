#!/usr/bin/env python
# 用于处理 google api 返回的数据

def handle_data(s_msg):
    title_list = []
    link_list = []
    for r_list in s_msg["items"]:
        title_list.append(r_list["title"])
        link_list.append(r_list["link"])
    # content = {"titles": title_list, "links": link_list}
    content = dict(zip(title_list, link_list))
    content = {"content": content}
    return content
