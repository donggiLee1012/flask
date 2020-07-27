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


from helloflask.module.youtube_comments import *

utube = Youtube('조블리',5,10)

utube.start()
