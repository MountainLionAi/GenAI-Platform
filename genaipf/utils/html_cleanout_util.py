from bs4 import BeautifulSoup,Comment


def cleanout(html_str):
    if html_str:
        soup = BeautifulSoup(html_str, 'html.parser')
        body = soup.body
        body.attrs = {}
        # 移除不需要的标签
        for tag in body.find_all(['svg', 'img', 'a', 'button', 'script', 'audio', 'video', 'iframe', 'object', 'embed', 'footer', 'header', 'noscript', 'style']):
            tag.decompose()
        # 移除空标签
        for tag in body.find_all(['span', 'div', 'li', 'p', 'i']):
            if not tag.text.strip():
                tag.decompose()
        # # 移除含有特定词汇的标签
        # keywords = ['breadcrumb', 'footer', 'header', 'download']
        # for tag in body.find_all(True):
        #     if tag is not None and tag.has_attr('class') and tag['class'] is not None:
        #         if any(keyword in ' '.join(tag['class']) for keyword in keywords):
        #             tag.decompose()
        #         else:
        #             for attr in list(tag.attrs) if tag.attrs else []:
        #                 if any(keyword in attr for keyword in keywords) or any(keyword in str(tag.attrs[attr] if tag.attrs else "") for keyword in keywords):
        #                     tag.decompose()
        #                     break
        # 移除所有标签的属性
        for tag in body.find_all(True):  # True匹配所有的tag
            tag.attrs = {}
        # 移除所有注释
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()
        content = body.decode_contents()
        return content
    return html_str



