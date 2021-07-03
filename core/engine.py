#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/26 下午4:05
# software: PyCharm
# project: lingzhi-engine
import logging

from kombu.utils import cached_property

logger = logging.getLogger('dongtai-engine')


class VulEngine(object):
    """
    根据策略和方法池查找是否存在漏洞，此类不进行策略和方法池的权限验证
    """

    def __init__(self):
        """
        构造函数，初始化相关数据
        """
        self._method_pool = None
        self.method_pool_asc = None
        self._vul_method_signature = None
        self.hit_vul = False
        self.vul_stack = None
        self.pool_value = None
        self.vul_source_signature = None
        self.graphy_data = {
            'nodes': [],
            'edges': []
        }
        self.method_counts = 0
        self.taint_link_size = 0
        self.edge_code = 1

    @property
    def method_pool(self):
        """
        方法池数据
        :return:
        """
        return self._method_pool

    @method_pool.setter
    def method_pool(self, method_pool):
        """
        设置方法池数据，根据方法调用ID对数据进行倒序排列，便于后续检索漏洞
        :param method_pool:
        :return:
        """
        self._method_pool = sorted(method_pool, key=lambda e: e.__getitem__('invokeId'), reverse=True)

    @property
    def vul_method_signature(self):
        return self._vul_method_signature

    @vul_method_signature.setter
    def vul_method_signature(self, vul_method_signature):
        self._vul_method_signature = vul_method_signature

    def prepare(self, method_pool, vul_method_signature):
        """
        对方法池、漏洞方法签名及其他数据进行预处理
        :param method_pool: 方法池，list
        :param vul_method_signature: 漏洞方法签名，str
        :return:
        """
        self.method_pool = method_pool
        self.vul_method_signature = vul_method_signature
        self.hit_vul = False
        self.vul_stack = list()
        self.pool_value = -1
        self.vul_source_signature = ''
        self.method_counts = len(self.method_pool)

    def hit_vul_method(self, method):
        if f"{method.get('className')}.{method.get('methodName')}" == self.vul_method_signature:
            self.hit_vul = True
            return True

    def do_propagator(self, method, current_link):
        is_source = method.get('source')
        target_hash = method.get('targetHash')

        for hash in target_hash:
            if hash in self.pool_value:
                if is_source:
                    current_link.append(method)
                    self.vul_source_signature = f"{method.get('className')}.{method.get('methodName')}"
                    return True
                else:
                    current_link.append(method)
                    self.pool_value = method.get('sourceHash')
                    break

    @cached_property
    def method_pool_signatures(self):
        signatures = set()
        for method in self.method_pool:
            signatures.add(f"{method.get('className').replace('/', '.')}.{method.get('methodName')}")
        return signatures

    def search(self, method_pool, vul_method_signature):
        self.prepare(method_pool, vul_method_signature)
        size = len(self.method_pool)
        for index in range(size):
            method = self.method_pool[index]
            if self.hit_vul_method(method):
                # 找到sink点所在方法，以此处为起点，寻找漏洞
                pass
            else:
                continue

            if 'sourceValues' in method:
                self.taint_value = method['sourceValues']
            # 找到sink点所在索引后，开始向后递归
            current_link = list()
            current_link.append(method)
            self.pool_value = set(method.get('sourceHash'))
            self.vul_source_signature = None
            logger.info(f'==> current taint hash: {self.pool_value}')
            if self.loop(index, size, current_link):
                break

    def loop(self, index, size, current_link):
        for sub_index in range(index + 1, size):
            sub_method = self.method_pool[sub_index]
            sub_target_hash = set(sub_method.get('targetHash'))
            if sub_target_hash and sub_target_hash & self.pool_value:
                if sub_method.get('source'):
                    current_link.append(sub_method)
                    self.vul_source_signature = f"{sub_method.get('className')}.{sub_method.get('methodName')}"
                    self.vul_stack.append(current_link[::-1])
                    current_link.pop()
                    return True
                else:
                    current_link.append(sub_method)
                    old_pool_value = self.pool_value
                    self.pool_value = set(sub_method.get('sourceHash'))
                    if self.loop(sub_index, size, current_link):
                        return True
                    self.pool_value = old_pool_value
                    current_link.pop()

    def search_sink(self, method_pool, vul_method_signature):
        self.prepare(method_pool, vul_method_signature)
        if vul_method_signature in self.method_pool_signatures:
            return True

    def dfs(self, current_hash, left_node, left_index):
        """
        深度优先搜索，搜索污点流图中的边
        :param current_hash: 当前污点数据，set()
        :param left_node: 上层节点方法的调用ID
        :param left_index: 上层节点方法在方法队列中的编号
        :return:
        """
        not_found = True
        for index in range(left_index + 1, self.method_counts):
            data = self.method_pool_asc[index]
            if current_hash & set(data['sourceHash']):
                not_found = False
                right_node = str(data['invokeId'])
                self.graphy_data['edges'].append({
                    'id': str(self.edge_code),
                    'source': left_node,
                    'target': right_node,
                })
                self.edge_code = self.edge_code + 1
                data['sourceHash'] = list(set(data['sourceHash']) - current_hash)
                self.dfs(set(data['targetHash']), right_node, index)

        if not_found:
            self.taint_link_size = self.taint_link_size + 1

    def create_node(self):
        """
        创建污点流图中使用的节点数据
        :return:
        """
        for data in self.method_pool_asc:
            source = ','.join([str(_) for _ in data['sourceHash']])
            target = ','.join([str(_) for _ in data['targetHash']])
            node = {
                'id': str(data['invokeId']),
                'name': f"{data['className'].replace('/', '.').split('.')[-1]}.{data['methodName']}({source}) => {target}",
                'dataType': 'source' if data['source'] else 'sql',
                'conf': [
                    {'label': 'source', 'value': source},
                    {'label': 'target', 'value': target},
                    {'label': 'caller', 'value': f"{data['callerClass']}.{data['callerMethod']}()"}
                ]
            }
            self.graphy_data['nodes'].append(node)

    def result(self):
        if self.vul_source_signature:
            return True, self.vul_stack, self.vul_source_signature, self.vul_method_signature, self.taint_value
        return False, None, None, None

    def get_taint_links(self):
        return self.graphy_data, self.taint_link_size, self.method_counts
