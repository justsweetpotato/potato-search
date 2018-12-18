#!/usr/bin/env python
# 用于处理 google api 返回的数据

def handle_data(s_msg):
    title_list = []
    link_list = []
    if s_msg.get("items"):  # 做判断, 以免输入不存在的书籍时服务器报500错误
        for r_list in s_msg["items"]:
            title_list.append(r_list["title"])
            link_list.append(r_list["link"])
        # content = {"titles": title_list, "links": link_list}
        data_dict = dict(zip(title_list, link_list))
        content = {"content": data_dict}
    else:
        content = None
    return content
