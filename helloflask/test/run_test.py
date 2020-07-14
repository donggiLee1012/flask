import os,sys
from helloflask.module.footsellcrawl import *

crawling = Footsell()

print(dir(crawling))

crawling.start('덩크')

pool_list=crawling.parser()

print(pool_list)