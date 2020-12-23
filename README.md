# disease-kb
# 常见疾病相关信息构建knowledge graph

**本项目根据从权威医药网站上爬取的医疗数据，对数据进行处理，从而运用到中文开放知识图谱（OpenKG.cn）中，以便需要者直接使用。**
**OpenKG链接：http://openkg.cn/dataset/disease-information**
 
**本项目借鉴前人智慧，但基于其爬取数据的方法对数据进行了更加充分的使用，https://github.com/liuhuanyong/QASystemOnMedicalKG 。**
 
**对获得的医疗数据进行整理，使其可直接用于知识图谱的搭建（Neo4j），文件处理成json格式。文件分为实体（实体基本信息与属性）和关系（不同实体间关系）两个类别。**
## 文件介绍
```shell
diseaseKB
├── data
│   └── medical.json 结构化疾病医疗知识
├── prepare_data
│   ├── build_data.py 数据处理到数据库
│   ├── data_spider.py 爬取数据
│   └── max_cut.py 根据给定的词典对文本进行前向、后向和双向最大匹配
├── dict 各种类别的词典
├── build_medicalgraph.py 利用结构化的数据建立Neo4j知识图谱 
├── build_medicalgraph_from_json.py 利用实体和关系json文件据建立知识图谱 
└── build_json.py 利用爬取的数据生成提炼的实体和关系json文件
```
### 使用方法
  1. 数据爬取与处理： data_spider.py -> build_data.py
  2. 知识图谱搭建（任意方式即可）： 
     - 原始文件搭建知识图谱： build_medicalgraph.py
     - 从生成实体关系文件到搭建知识图谱： build_json.py -> build_medicalgraph_from_json.py
## 数据获取与处理
### 获取
  数据从“寻医问药”医疗网站上爬取原始数据，将其保存到本地数据库（mongodb)中。爬取数据以疾病为单位，获得其各方面的信息，如：成因、症状、服用药物等。爬取时，根据疾病id爬取不同的网站。除疾病外，还爬取了疾病监测的相关数据，也将其保存到数据库中。
### 处理
  对爬取的数据进行预处理，筛选适合做知识图谱知识存储的相关信息。最后从数据库中提取出结构化的文件medical.json,用于搭建知识图谱。数据大致信息如下：
  <p align="left">
	<img src=./pic/json.png alt="Sample"  width="500">
	<p align="center">
		<em> </em>
	</p>
</p>

## 知识图谱
  利用结构化的知识，选择相关内容作为实体、关系与属性，搭建Neo4j上的知识图谱。为方便使用，将搭建图谱的实体、关系与属性保存为json格式，即方便搭建知识图谱，也利于阅读。
### 搭建
 - medical.json为从数据中导出的整理后的疾病医疗数据，读取该文件获得各类别的实体、关系，从而搭建知识图谱。
 - 同时，也可以先从medical.json提炼出实体与关系的json文件，再通过这两个文件生成知识图谱。且生成的文件可读性更高。
 - 这两种生成的知识图谱等价。
 - 搭建后的知识图谱统计信息如下：
 1. 知识图谱实体类型（8类实体）
 
| 实体类型   |   中文含义   | 实体数量 | 举例                                   |
| :--------- | :----------: | :------: | :-------------------------------------|
| Disease    |     疾病     |  8808    | 急性肺脓肿                             |
| Drug       |     药品     |  3828    | 布林佐胺滴眼液                         |
| Food       |     食物     |  4870    | 芝麻                                   |
| Check      |   检查项目   |  3353    | 胸部CT检查                             |
| Department |     科目     |  54      | 内科                                   |
| Producer   |   在售药品   |  17,201  | 青阳醋酸地塞米松片                     |
| Symptom    |   疾病症状   |  5,998   | 乏力                                   |
| Cure       |   治疗方法   |  544     | 抗生素药物治疗                         |
| Total      |     总计     |  44,656  | 约4.4万实体量级                        |

2. 疾病实体属性类型（7类属性）

| 属性类型      |   中文含义   |            举例             |
| :------------ | :----------: | :-------------------------: |
| name          |   疾病名称   |       成人呼吸窘迫综合征        |
| desc          |   疾病简介   |    成人呼吸窘迫综合征简称ARDS...    |
| cause         |   疾病病因   |    化脓性感染可使细菌毒素...    |
| prevent       |   预防措施   | 对高危的患者应严密观察... |
| cure_lasttime |   治疗周期   |          2-4月          |
| cured_prob    |   治愈概率   |             85%             |
| easy_get      | 疾病易感人群 |        无特定的人群         |

3. 知识图谱关系类型（11类关系）
 
| 实体关系类型   |   中文含义   | 关系数量 | 举例                                                 |
| :------------- | :----------: | :------: | :--------------------------------------------------- |
| belongs_to     |     属于     |  8,843   | <内科,属于, 呼吸内科>                                   |
| common_drug    | 疾病常用药品 |  14,647  | <成人呼吸窘迫综合征,常用, 人血白蛋白>                    |
| do_eat         | 疾病宜吃食物 |  22,230  | <成人呼吸窘迫综合征,宜吃,莲子>                                 |
| drugs_of       | 药品在售药品 |  17,315  | <人血白蛋白,在售,莱士人蛋白人血白蛋白>               |
| need_check     | 疾病所需检查 |  39,418  | <单侧肺气肿,所需检查,支气管造影>                     |
| no_eat         | 疾病忌吃食物 |  22,239  | <成人呼吸窘迫综合征,忌吃, 啤酒>                                     |
| recommand_drug | 疾病推荐药品 |  59,465  | <混合痔,推荐用药,京万红痔疮膏>                       |
| recommand_eat  | 疾病推荐食谱 |  40,221  | <成人呼吸窘迫综合征,推荐食谱,百合糖粥>                 |
| has_symptom    |   疾病症状   |  54,710  | <成人呼吸窘迫综合征,疾病症状,呼吸困难>                   |
| acompany_with  | 疾病并发疾病 |  12,024  | <成人呼吸窘迫综合征,并发疾病,细菌性肺炎>  |
| cure_way       | 疾病治疗方法 |  21，047 | <急性肺脓肿,治疗方法,抗生素药物治疗>  |
| Total          |     总计     | 312,159  | 约31万关系量级                                       |
 
### 文件介绍
  生成的实体和关系的json文件分别为entities.json和relations.json。
  1. entities.json文件说明
  - 此文件包含8类实体，其中疾病（‘Disease’）相较其他实体有额外的属性，而其他类实体无其他属性，如下图。
  <p align="left">
	<img src=./pic/ent0.PNG alt="Sample"  width="400">
	<p align="center">
		<em> </em>
	</p>
</p>
  <p align="left">
	<img src=./pic/ent1.PNG alt="Sample"  width="250">
	<p align="center">
		<em> </em>
	</p>
</p>
  2. relations.json文件说明
  - 此文件包含11类关系，每一类关系为一个字典，信息包括开始实体类型、结束实体类型、关系类型、关系名称、关系集合，关系集合中包括了该类关系的所有关系，信息包括开始实体名称与结束实体名称，如下图。
    <p align="left">
	<img src=./pic/rel0.PNG alt="Sample"  width="350">
	<p align="center">
		<em> </em>
	</p>
</p>
    <p align="left">
	<img src=./pic/rel1.PNG alt="Sample"  width="450">
	<p align="center">
		<em> </em>
	</p>
</p>

### 图谱效果
  实现了Neo4j上的知识图谱，下图为某一检索效果：
    <p align="left">
	<img src=./pic/graph.png alt="Sample"  width="500">
	<p align="center">
		<em> </em>
	</p>
</p>
