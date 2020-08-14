# import os,sys
# from helloflask.module.footsellcrawl import *
#
# crawling = Footsell()
#
# print(dir(crawling))
#
# crawling.start('덩크')
#
# pool_list=crawling.parser()
#
# print(pool_list)

from flask import url_for


import os,sys

from helloflask.module.youtube_comments import *

utube = Youtube('여행브이로그',5,6)

thumbnail=[]
pool=[]
comment_list=[]

contents = utube.search(thumbnail)
for i in contents:
    try:
        comments = utube.comment_parser(utube.utuber_parser(i,pool))
        comment_list.append(comments)
    except:
        pass

href_count = 0
mk_row = ''
for yongsang in comment_list:

    for row in yongsang:
        mk_row += '''
<tr>
<td><a href="{url}">{youtuber}</a></td>
<td>{name}</td>
<td>{comments}</td>
<td>{like}</td>
<td>{update}</td>
</tr>       
        '''.format(name=row[0],
                   comments=row[1],
                   like=row[2],
                   youtuber=row[3],
                   update=row[4], url=contents[href_count])

    href_count += 1

print(utube.driverpath)
print(mk_row)