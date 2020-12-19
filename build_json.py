# coding: utf-8


import os
import json
# from py2neo import Graph,Node

class MedicalGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, 'data/medical.json')

    '''读取文件'''
    def read_nodes(self):
        # 共７类节点
        drugs = [] # 药品
        foods = [] #　食物
        checks = [] # 检查
        departments = [] #科室
        producers = [] #药品大类
        diseases = [] #疾病
        symptoms = []#症状

        disease_infos = []#疾病信息

        # 构建节点实体关系
        rels_department = [] #　科室－科室关系（前小后大）
        rels_noteat = [] # 疾病－忌吃食物关系
        rels_doeat = [] # 疾病－宜吃食物关系
        rels_recommandeat = [] # 疾病－推荐吃食物关系
        rels_commonddrug = [] # 疾病－通用药品关系
        rels_recommanddrug = [] # 疾病－热门药品关系
        rels_check = [] # 疾病－检查关系
        rels_drug_producer = [] # 厂商－药物关系

        rels_symptom = [] #疾病症状关系
        rels_acompany = [] # 疾病并发关系
        rels_category = [] #　疾病与科室之间的关系


        count = 0
        for data in open(self.data_path,'rb'):
            disease_dict = {}
            count += 1
            print(count)
            data_json = json.loads(data)
            disease = data_json['name']
            disease_dict['name'] = disease
            diseases.append(disease)
            disease_dict['desc'] = ''
            disease_dict['prevent'] = ''
            disease_dict['cause'] = ''
            disease_dict['easy_get'] = ''
            disease_dict['cure_department'] = ''
            disease_dict['cure_way'] = ''
            disease_dict['cure_lasttime'] = ''
            disease_dict['symptom'] = ''
            disease_dict['cured_prob'] = ''

            if 'symptom' in data_json:
                symptoms += data_json['symptom']
                for symptom in data_json['symptom']:
                    rels_symptom.append([disease, symptom])

            if 'acompany' in data_json:
                for acompany in data_json['acompany']:
                    rels_acompany.append([disease, acompany])

            if 'desc' in data_json:
                disease_dict['desc'] = data_json['desc']

            if 'prevent' in data_json:
                disease_dict['prevent'] = data_json['prevent']

            if 'cause' in data_json:
                disease_dict['cause'] = data_json['cause']

            if 'get_prob' in data_json:
                disease_dict['get_prob'] = data_json['get_prob']

            if 'easy_get' in data_json:
                disease_dict['easy_get'] = data_json['easy_get']

            if 'cure_department' in data_json:
                cure_department = data_json['cure_department']
                if len(cure_department) == 1:
                     rels_category.append([disease, cure_department[0]])
                if len(cure_department) == 2:
                    big = cure_department[0]
                    small = cure_department[1]
                    rels_department.append([small, big])
                    rels_category.append([disease, small])

                disease_dict['cure_department'] = cure_department
                departments += cure_department

            if 'cure_way' in data_json:
                disease_dict['cure_way'] = data_json['cure_way']

            if  'cure_lasttime' in data_json:
                disease_dict['cure_lasttime'] = data_json['cure_lasttime']

            if 'cured_prob' in data_json:
                disease_dict['cured_prob'] = data_json['cured_prob']

            if 'common_drug' in data_json:
                common_drug = data_json['common_drug']
                for drug in common_drug:
                    rels_commonddrug.append([disease, drug])
                drugs += common_drug

            if 'recommand_drug' in data_json:
                recommand_drug = data_json['recommand_drug']
                drugs += recommand_drug
                for drug in recommand_drug:
                    rels_recommanddrug.append([disease, drug])

            if 'not_eat' in data_json:
                not_eat = data_json['not_eat']
                for _not in not_eat:
                    rels_noteat.append([disease, _not])

                foods += not_eat
                do_eat = data_json['do_eat']
                for _do in do_eat:
                    rels_doeat.append([disease, _do])

                foods += do_eat
                recommand_eat = data_json['recommand_eat']

                for _recommand in recommand_eat:
                    rels_recommandeat.append([disease, _recommand])
                foods += recommand_eat

            if 'check' in data_json:
                check = data_json['check']
                for _check in check:
                    rels_check.append([disease, _check])
                checks += check
            if 'drug_detail' in data_json:
                drug_detail = data_json['drug_detail']
                producer = [i.split('(')[0] for i in drug_detail]
                rels_drug_producer += [[i.split('(')[0], i.split('(')[-1].replace(')', '')] for i in drug_detail]
                producers += producer
            disease_infos.append(disease_dict)
        return set(drugs), set(foods), set(checks), set(departments), set(producers), set(symptoms), set(diseases), disease_infos,\
               rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug,\
               rels_symptom, rels_acompany, rels_category

    '''建立节点'''
    def create_node(self, label, nodes):
        count = 0
        en_list=[]
        for node_name in nodes: #将结点集中的结点设置为
            item={}
            item[label]=node_name
            # node = Node(label, name=node_name)
            # self.g.create(node)
            count += 1
            print(count, len(nodes))
            en_list.append(item)
        return en_list

    '''创建知识图谱实体节点类型schema'''
    def create_graphnodes(self):
        Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, disease_infos,rels_check, \
        rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, \
        rels_recommanddrug,rels_symptom, rels_acompany, rels_category = self.read_nodes()
        entities = []
        l=self.create_node('Diseases',Diseases)
        entities.extend(l)
        l=self.create_node('Drug', Drugs)
        entities.extend(l)
        print(len(Drugs))
        l=self.create_node('Food', Foods)
        entities.extend(l)
        print(len(Foods))
        l=self.create_node('Check', Checks)
        entities.extend(l)
        print(len(Checks))
        l=self.create_node('Department', Departments)
        entities.extend(l)
        print(len(Departments))
        l=self.create_node('Producer', Producers)
        entities.extend(l)
        print(len(Producers))
        l=self.create_node('Symptom', Symptoms)
        entities.extend(l)
        filename='newdata/entities.json'
        json.dump(entities, open(filename, 'w', encoding='utf-8'), indent=4, ensure_ascii=False)
        return


    '''创建实体关系边'''
    def create_graphrels(self):
        Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, disease_infos, rels_check,\
        rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, \
        rels_drug_producer, rels_recommanddrug,rels_symptom, rels_acompany, rels_category = self.read_nodes()
        self.create_relationship('Disease', 'Food', rels_recommandeat, 'recommand_eat', '推荐食谱')
        self.create_relationship('Disease', 'Food', rels_noteat, 'no_eat', '忌吃')
        self.create_relationship('Disease', 'Food', rels_doeat, 'do_eat', '宜吃')
        self.create_relationship2('Department', 'Department', rels_department, 'belongs_to', '属于','Disease', 'Department', rels_category, 'belongs_to', '所属科室')
        self.create_relationship('Disease', 'Drug', rels_commonddrug, 'common_drug', '常用药品')
        self.create_relationship('Producer', 'Drug', rels_drug_producer, 'drugs_of', '生产药品')
        self.create_relationship('Disease', 'Drug', rels_recommanddrug, 'recommand_drug', '好评药品')
        self.create_relationship('Disease', 'Check', rels_check, 'need_check', '诊断检查')
        self.create_relationship('Disease', 'Symptom', rels_symptom, 'has_symptom', '症状')
        self.create_relationship('Disease', 'Disease', rels_acompany, 'acompany_with', '并发症')

    '''创建实体关联边'''
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        filename='newdata/'+rel_type+'.json'
        rels=[]
        count = 0

        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            item={}
            item['start_entity_type']=start_node
            item['end_entity_type']=end_node
            item['start_entity_name']=p
            item['end_entity_name']=q
            item['rel_type']=rel_type
            item['rel_name']=rel_name
            count += 1
            print(rel_type, count, all)
            rels.append(item)

        json.dump(rels,open(filename,'w',encoding='utf-8'),indent=4,ensure_ascii=False)
        return

    def create_relationship2(self, start_node, end_node, edges, rel_type, rel_name, start_node2, end_node2, edges2, rel_type2, rel_name2):
        filename = 'newdata/' + rel_type + '.json'
        rels = []

        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        count = 0
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            item={}
            item['start_entity_type']=start_node
            item['end_entity_type']=end_node
            item['start_entity_name']=p
            item['end_entity_name']=q
            item['rel_type']=rel_type
            item['rel_name']=rel_name
            count += 1
            print(rel_type, count, all)
            rels.append(item)

        set_edges = []
        for edge in edges2:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        count = 0
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            item = {}
            item['start_entity_type'] = start_node2
            item['end_entity_type'] = end_node2
            item['start_entity_name'] = p
            item['end_entity_name'] = q
            item['rel_type'] = rel_type2
            item['rel_name'] = rel_name2
            count += 1
            print(rel_type2, count, all)
            rels.append(item)

        json.dump(rels,open(filename,'w',encoding='utf-8'),indent=4,ensure_ascii=False)
        return

if __name__ == '__main__':
    handler = MedicalGraph()
    handler.create_graphnodes()
    handler.create_graphrels()

