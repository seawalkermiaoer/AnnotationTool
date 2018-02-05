# -*- coding:utf-8 -*-
# __author__ = 'xianghai'
import json

from getBaiduZhidao import getQuestion


def persist(path, content):
    with open(path, mode='a', encoding='utf-8') as fo:
        tmp = json.dumps(content, ensure_ascii=False)
        fo.write(tmp + '\n')

if __name__ == '__main__':
    for i in range(0, 29):
        with open('data/to_be_labelled/part_%d.json' % i, mode='r', encoding='utf-8') as fi:
            lines = fi.readlines()
            status = {
                'size': len(lines),
                'ok': 0,
                'fail': 0,
                'sim_status': {}
            }

            for l in lines:
                ret = {}
                tmp = json.loads(l.strip('\n'), encoding='utf-8')
                rsp = getQuestion(question=tmp['question'])
                if rsp['issuccess']:
                    status['ok'] += 1
                else:
                    status['fail'] += 1
                sim_size_tag = str(len(rsp['data']))
                if sim_size_tag not in status['sim_status']:
                    status['sim_status'].update({sim_size_tag: 0})
                status['sim_status'][sim_size_tag] += 1
                if rsp['issuccess']:
                    ret.update(tmp)
                    ret.update(rsp)
                    persist('data/input/part_%d.json' % i, ret)
        print(i, status)


