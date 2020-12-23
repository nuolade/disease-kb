# coding: utf-8


import os
import json
from py2neo import Graph,Node

class MedicalGraphFromJson:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, 'newdata')
        self.g = Graph(
            host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            http_port=7474,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="123456")
        # self.rel_files=[]
        # self.init_rel_files()
        self.rel_file='relations.json'
        self.node_file='entities.json'

    # def init_rel_files(self):
    #     files=[
    #         'need_check.json',
    #         'has_symptom.json',
    #         'cure_way.json',
    #         'acompany_with.json',
    #         'recommand_drug.json',
    #         'drugs_of.json',
    #         'do_eat.json',
    #         'common_drug.json',
    #         'belongs_to_0.json',
    #         'belongs_to_1.json',
    #         'recommand_eat.json',
    #         'no_eat.json'
    #     ]
    #     self.rel_files=files

    def build_graph(self):
        res=self.build_nodes()
        if res==-1:
            print('no nodes file, can not create relations')
            return
        self.build_rels()

    def build_nodes(self):
        node_file=os.path.join(self.data_path,self.node_file)
        if not os.path.exists(node_file):
            return -1
        nodes=json.load(open(node_file))
        for node in nodes:
            self.create_node(node)
        return 0

    def create_node(self,node):
        label=node['label']
        if label == 'Disease':
            n=Node(label,name=node['name'])
        else:
            n=Node(label,name=node['name'],desc=node['desc'],
                        prevent=node['prevent'] ,cause=node['cause'],
                        easy_get=node['easy_get'],cure_lasttime=node['cure_lasttime'],
                        cured_prob=node['cured_prob'])
        self.g.create(n)

    def build_rels(self):
        rel_file=os.path.join(self.data_path,self.rel_file)
        if not os.path.exists(rel_file):
            print(self.rel_file,'not exist, skip')
            return
        relations=json.load(open(rel_file))
        for rel in relations:
            self.create_rel(rel)
        # for file in self.rel_files:
        #     rel_file = os.path.join(self.data_path, file)
        #     if not os.path.exists(rel_file):
        #         print(file, 'not exist, skip')
        #         continue
        #     rels_set = json.load(open(rel_file))
        #     self.create_rel(rels_set)

    def create_rel(self,rels_set):
        cnt=0
        start_entity_type=rels_set['start_entity_type']
        end_entity_type=rels_set['end_entity_type']
        rel_type=rels_set['rel_type']
        rel_name=rels_set['rel_name']
        rels=rels_set['rels']
        for rel in rels:
            p=rel['start_entity_name']
            q=rel['end_entity_name']
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_entity_type, end_entity_type, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                cnt+=1
                print(rel_type,cnt,len(rels))
            except Exception as e:
                print(e)
        return

if __name__ == '__main__':
    handler = MedicalGraphFromJson()
    handler.build_graph()

