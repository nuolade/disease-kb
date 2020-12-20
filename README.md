# disease-kb
# 常见疾病相关信息构建knowledge graph

**本项目根据从权威医药网站上爬取的医疗数据，对数据进行处理，从而运用到中文开放知识图谱（OpenKG.cn）中，以便需要者直接使用。**
**OpenKG链接：http://openkg.cn/dataset/disease-information**
 
**本项目借鉴前人智慧，但基于其爬取数据的方法对数据进行了更加充分的使用，https://github.com/baiyang2464/chatbot-base-on-Knowledge-Graph。**
 
**对获得的医疗数据进行整理，使其可直接用于知识图谱的搭建（Neo4j），文件处理成json格式。文件分为实体（实体基本信息）、关系（不同实体间关系）和属性（实体的属性信息）三个类别。**
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
└── build_json.py
```


## 数据获取与处理
### 获取
  数据从“寻医问药”医疗网站上爬取原始数据，将其保存到本地数据库中。爬取会以疾病为单位，爬取其相应的信息，如：成因、症状、服用药物等信息。爬取一个疾病各个方面的信息，需根据疾病id去不同的网站爬取。除疾病外，还爬取了疾病监测的相关数据，也将其保存到数据库中。
### 处理
  对爬取的数据进行预处理，筛选适合做知识图谱知识存储的相关信息。最后从数据库中提取出结构化的文件medical.json,用于搭建知识图谱。数据大致信息如下：
  <p align="left">
	<img src=./pic/json.png alt="Sample"  width="500">
	<p align="center">
		<em> </em>
	</p>
</p>

## 知识图谱
  利用结构化的知识，选择相关内容作为实体、关系与属性，搭建Neo4j上的知识图谱。为方便直接搭建图谱，将搭建图谱的实体、关系与属性保存为json格式，方便使用。
### 搭建
### 文件介绍
