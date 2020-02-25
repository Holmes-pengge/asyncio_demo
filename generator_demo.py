import os
import fnmatch
import gzip
import bz2
import re


##################
# 参考来源 https://python3-cookbook.readthedocs.io/zh_CN/latest/c04/p13_create_data_processing_pipelines.html
##################

class SelfGenerator:
    """一个由多个执行特定任务、独立任务的简单生成器函数组成的容器"""

    def gen_find(self, filepat, top):
        """
        在目录树中查找与shell 通配符模式匹配的所有文件名
        """
        for path, dirlist, filelist in os.walk(top):
            for name in fnmatch.filter(filelist, filepat):
                yield os.path.join(path, name)

    def gen_opener(self, filenames):
        """
        一次打开一个文件名序列，生成一个文件对象。
         进行下一个迭代时，文件将立即关闭。
        """
        for filename in filenames:
            if filename.endswith('.gz'):
                f = gzip.open(filename, 'rt')
            elif filename.endswith('.bz2'):
                f = bz2.open(filename, 'rt')
            else:
                f = open(filename, 'rt')
            yield f
            f.close()

    def gen_concatenate(self, iterators):
        """
        将一个迭代器序列链接到一个序列中。
        """
        for it in iterators:
            yield from it

    def gen_grep(self, pattern, lines):
        """
        在一系列行中查找正则表达式模式
        """
        pat = re.compile(pattern)
        for line in lines:
            if pat.search(line):
                yield line


if __name__ == '__main__':
    gen = SelfGenerator()
    lognames = gen.gen_find('access-log*', 'www')
    files = gen.gen_opener(lognames)
    lines = gen.gen_concatenate(files)
    pylines = gen.gen_grep('(?i)python', lines)
    for line in pylines:
        print(line)
