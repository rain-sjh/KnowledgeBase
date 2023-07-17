from configparser import ConfigParser
from os import listdir
from os.path import dirname, abspath, join


# 获取根目录
def root_path():
    return dirname(cur_path())


# 获取当前目录
def cur_path():
    return dirname(abspath(__file__))


# 获取配置目录
def config_path():
    return '%s\\config\\' % root_path()


# 获取配置
# 如仅有一个传参,返回默认配置
# 如有两个传参,参数一为配置名
def config(name, sections=''):
    conf = ConfigParser()
    # 获取所有配置文件
    filelist = listdir(config_path())
    for filename in filelist:
        if filename != 'default.ini':
            filepath = join(config_path(), filename)
            # 读取配置文件
            conf.read(filepath, encoding='utf-8')
            # 有两个参数时
            if sections and conf.has_option(name, sections):
                return conf[name].get(sections)
            # 仅name时
            for key in conf.sections():
                if conf.has_option(key, name):
                    return conf.get(key, name)

    filepath = join(config_path(), 'default.ini')
    conf.read(filepath, encoding='utf-8')
    if conf.has_option('default', name):
        return conf.get('default', name)
