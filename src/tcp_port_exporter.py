#! /usr/bin/env python
# -*- coding:utf-8 -*-
import socket
# import threading
# import configparser
from tornado.web import RequestHandler, Application, iostream
from prometheus_client.core import GaugeMetricFamily, _floatToGoString


def try_connect(ip, port):
    """
    try socket to connect ip:port
    :param ip:
    :param port:
    :return: True or False
    """
    s = socket.socket()
    # print("Attempting to connect to %s on port %s" % (ip, port))
    try:
        s.connect((ip, int(port)))
        # print("Connected to %s on port %s" % (ip, port))
        # print(ip, port, True)
        return (ip, port, 1)
    except socket.error as e:
        print("Connected to %s on port %s failed: %s" % (ip, port, e))
        # print(ip, port, False)
        return (ip, port, 0)


def target_list(file='check_tcp_port.list'):
    """
    read target ip:port from file.Default file is ./check_tcp_port.list
    :param file:
    :return: ip port list
    """
    targets = []
    # file 方式
    try:
        with open(file, 'rb') as f:
            for line in f.readlines():
                line = line.strip()  # strip() 参数为空时，默认删除空白符（包括'\n', '\r',  '\t',  ' ')
                if line != '':  # 去除空白行
                    target = str(line).split('--')[1].split(':')
                    targets.append(tuple(target))
    except Exception as e:
        print(e)

    # config parser 方式
    # c = configparser.ConfigParser()
    # c.read(file)
    # for key in c.keys():
    #     if not key == 'DEFAULT':
    #         targets.append(tuple(c.get(key, 'target').split(':')))
    return targets


def gen_metrics():
    metrics = {}
    targets = target_list()
    # for args in targets:
    #     print(try_connect(*args))

    for target in targets:
        metric_key = '_'.join(target)
        # print(metric_key)  # 192.168.104.110_9101
        metrics[metric_key] = GaugeMetricFamily('check_tcp_port', '# 端口存活监测', labels=['host', 'port'])

        # add metric value
        check_result = try_connect(*target)
        metrics[metric_key].add_metric([target[0], target[1]], check_result[2])

    # print(metrics)
    for name, metric in metrics.items():
        yield metric


def generate_latest():
    output = []
    for metric in gen_metrics():
        # print('metric.name -->', metric.name)
        # print('metric.documentation -->', metric.documentation)
        # print('metric.samples -->', metric.samples)
        output.append('# HELP {0} {1}'.format(
            metric.name, metric.documentation.replace('\\', r'\\').replace('\n', r'\n')))
        output.append('\n# TYPE {0} {1}\n'.format(metric.name, metric.type))
        for name, labels, value in metric.samples:
            if labels:
                labelstr = '{{{0}}}'.format(','.join(
                    ['{0}="{1}"'.format(
                        k, v.replace('\\', r'\\').replace('\n', r'\n').replace('"', r'\"'))
                        for k, v in sorted(labels.items())]))
            else:
                labelstr = ''
            output.append('{0}{1} {2}\n'.format(name, labelstr, _floatToGoString(value)))
        # print(metric)
    # print(''.join(output))
    return ''.join(output)


class ChechTcpPortHandler(RequestHandler):
    def get(self):
        self.post()

    def post(self):
        self.set_header('Content-Type', 'text/plain; charset=UTF-8')
        output = generate_latest()
        self.write(output)


def http_main():
    port = 1990
    address = socket.gethostbyname(socket.gethostname())
    handlers = [
        (r"/metrics", ChechTcpPortHandler),

    ]
    settings = dict(page_title=u"-imip-master-webserver-", )
    app = Application(handlers=handlers, **settings)
    app.listen(port=port, address=address)
    iostream.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    # generate_latest()
    # print(tcp_port_list())
    http_main()
