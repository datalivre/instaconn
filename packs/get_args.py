# _*_ coding:utf-8 _*_
# @author Robert Carlos                 #
# email robert.carlos@linuxmail.org     #
# 2019-Dec (CC BY 3.0 BR)               #

import errno
from os import path
from sys import exit


def get_args(filename):

    if path.isfile(filename):
        dict_properties = {}
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    if '#' not in line:
                        tmplist = [l.strip() for l in line.split('=')]
                        dict_properties[tmplist.pop(0)] = tmplist[1]
            return dict_properties
        except IOError:
            print(f'Erro ao manipular {filename}')
            exit(errno.EPERM)
    else:
        print(f'Arquivo {filename} não encontrado.')
        exit(errno.EPERM)


if __name__ == "__main__":
    filename = 'instaconn.properties'
    print(get_args(filename))
