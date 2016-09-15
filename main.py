# coding:utf8

from getImgs import getImgs

def start_transfer(path):
    ToPath = path + '_include_image'
    zh = getImgs(path, ToPath)
    zh.start()

