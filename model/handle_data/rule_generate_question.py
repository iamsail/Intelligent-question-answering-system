#!usr/bin/python
# -*- coding:utf-8 -*-
""" 用于生成问题的规则和NLP部分

@author: Sail
@contact: 865605793@qq.com
@github: https://github.com/iamsail/Intelligent-question-answering-system
"""


# 引入词性标注接口
import jieba.posseg as psg

# 生成问题 结合row_tags.txt进行分析,设计规则

# 这一步最为重要，基于规则目前考虑了以下几种情况：
#
# 规则1、假如只有一个有用标签或最后一个标签包含“简介”，则直接使用“什么是… …？”来生成问题。如：“帮助中心 > 机器学习服务”。
#
# 规则2: 若最后一个标签已?/？结尾,则直接将最后一个标签提取为问题
#
#
# 三、假如最后一个标签是“概述”或者“产品概述”，则用第一个标签和倒数第二个标签生成问题。如：“帮助中心 > 机器学习服务 > 产品介绍 > 产品概述”。
#
# 四、假如最后一个标签在例外情况（动词做定语开头）之中，则用“… …有哪些？”生成问题。如：“帮助中心 > 机器学习服务 > 使用限制”。
#
# 五、假如最后一个标签的最后一个词为管理，则用“怎么管理… …?”生成问题。如：“帮助中心 > 云容器引擎 > 用户指南 > 操作指南 > 存储管理”。
#
# 六、假如最后一个标签以动词开头，使用“怎么… …”来生成问题。如：“帮助中心 > 镜像服务 > 用户指南 > 管理 > 共享镜像”。
#
# 七、假如最后一个标签为”与… …”，使用第一个标签和最后一个标签形成问句。如：“帮助中心 > 镜像服务 > 用户指南 > 管理 > 与容器的关系”
#
# 八、假如最后一个标签以动词、形容词开头，使用“… …有哪些”来生成。如：“帮助中心 > 镜像服务 > 用户指南 > 管理”。
#
# 目前存在这几种问题有待解决：
#
# 一、仍然有些动词做定语开头的标签没有添加进情况四中。
#
# 二、有些标签以名词、形容词开头但是不能用“… …有哪些”来问。如“可视化”，“场景说明”。解决方法有待研究。
#
# 三、某些标签以其他词开头，如英文。解决方法有待研究。

def rule1(wordPairs, tagList):
    """　基于规则1生成问题

    规则1: 假如只有一个有用标签，则直接使用“什么是… …？”来生成问题。如：“帮助中心 > 机器学习服务”。
     or 假如最后一个标签包含“简介”，则直接使用“什么是… …？”来生成问题。如：“帮助中心 > 机器学习服务”。

    Args:
       wordPairs: 分词后的单词与词性对
       tagList: 问题标签(Q)集合

    Returns:
       question: 提取出的问题
    """
    question = ''
    if len(wordPairs) == 1:
        question = "什么是%s?"%(str(wordPairs).split('/')[0])
    elif '简介' in wordPairs[len(wordPairs) - 1]:
        question = "%s是什么?"%(tagList[len(tagList) - 1])

    return question



def rule2(wordPairs, tagList):
    """　基于规则2生成问题

        规则2: 假如最后一个标签的开头是疑问词，则不需要生成问题。如：“帮助中心 > 机器学习服务 > 什么是机器学习服务”。

        Args:
           wordPairs: 分词后的单词与词性对
           tagList: 问题标签(Q)集合

        Returns:
           question: 提取出的问题
        """
    question = ''
    lastChar = str(wordPairs[len(wordPairs) - 1]).split('/')[0]
    if lastChar == '?' or lastChar == '？':
        question = tagList[len(tagList) - 1]

    return question




def rule3(wordPairs, tagList):
    """假如最后一个标签是“概述”或者“产品概述”，则用第一个标签和倒数第二个标签生成问题。如：“帮助中心 > 机器学习服务 > 产品介绍 > 产品概述”。

    """
    question = ''
    lastChar = str(wordPairs[len(wordPairs) - 1]).split('/')[0]

    if lastChar == '概述':
        question = tagList[0] + tagList[-2]
    return question



def rule5(wordPairs, tagList):
    """假如最后一个标签的最后一个词为管理，则用“怎么管理… …?”生成问题。如：“帮助中心 > 云容器引擎 > 用户指南 > 操作指南 > 存储管理”

    """
    question = ''
    lastChar = str(wordPairs[len(wordPairs) - 1]).split('/')[0]

    if lastChar == '管理':
        question = '怎么管理%s' % (tagList[0])

    return question


def rule6(wordPairs, tagList):
    """ 假如最后一个标签以动词开头，使用“怎么… …”来生成问题。如：“帮助中心 > 镜像服务 > 用户指南 > 管理 > 共享镜像”。

    """
    question = ''
    seg = psg.cut(tagList[-1])
    v_word = ''
    n_word = ''
    for i,ele in enumerate(seg):
        if i == 0 and str(ele).split('/')[1] == 'v':
            v_word = str(ele).split('/')[0]
            n_word = str(tagList[-1])[len(v_word):]

    if v_word:
        question = '怎样%s%s的%s' % (v_word, tagList[0], n_word)

    return question


def rule7(wordPairs, tagList):
    """ 假如最后一个标签为”与… …”，使用第一个标签和最后一个标签形成问句。如：“帮助中心 > 镜像服务 > 用户指南 > 管理 > 与容器的关系”

    """
    question = ''

    if '与' == tagList[-1][0]:
        question = '%s%s' % (tagList[0], tagList[-1])

    return question



def get_Q_by_rules(wordPairs, tagList):
    """　基于规则生成问题,遍历所有规则

    Args:
       wordPairs: 分词后的单词与词性对
       tagList: 问题标签(Q)集合
    Returns:
       question: 提取出的问题
    """

    question = ''
    if(rule1(wordPairs, tagList)):
        question = rule1(wordPairs, tagList)

    elif(rule2(wordPairs, tagList)):
        question = rule2(wordPairs, tagList)

    elif(rule3(wordPairs, tagList)):
        question = rule3(wordPairs, tagList)

    elif(rule5(wordPairs, tagList)):
        question = rule5(wordPairs, tagList)

    elif(rule6(wordPairs, tagList)):
        question = rule6(wordPairs, tagList)

    elif(rule7(wordPairs, tagList)):
        question = rule7(wordPairs, tagList)

    # if question != '':
    #     print(question)

    return question
    # if question:
    #     print(question)



