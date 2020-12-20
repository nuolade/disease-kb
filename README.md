# disease-kb
# 常见疾病相关信息构建knowledge graph

 **本项目根据从权威医药网站上爬取的医疗数据，对数据进行处理，从而运用到中文开放知识图谱（OpenKG.cn）中，以便需要者直接使用。**
 
 **本项目借鉴前人智慧，https://github.com/baiyang2464/chatbot-base-on-Knowledge-Graph ，但基于其爬取数据的方法对数据进行了更加充分的使用。**
 
 **对获得的医疗数据进行整理，使其可直接用于知识图谱的搭建（Neo4j），文件处理成json格式。文件分为实体（实体基本信息）、关系（不同实体间关系）和属性（实体的属性信息）三个类别。
