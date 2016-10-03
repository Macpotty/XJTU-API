# -*- coding: utf-8 -*-
# @Author: Michael
# @Date:   2016-10-04 01:01:58
# @Last Modified by:   Michael
# @Last Modified time: 2016-10-04 01:31:56
import requests


class BaseUtil(object):
    """docstring for BaseUtil"""
    def __init__(self, soup):
        super(BaseUtil, self).__init__()
        self._soup = soup

    def update(self, soup):
        self._soup = soup


class TeachingAssessUtil(BaseUtil):
    def __init__(self, soup):
        super(TeachingAssessUtil, self).__init__()
        self._soup = soup

    def assessmentsGen(self):
        assessments = {}
        for item in self._soup.find('table', attrs={'class': 'portlet-table'}).tr.find_all('td', style='vertical-align:middle'):
            assessments[item.div.input.get('name')] = item.div.input.get('value')
        return assessments

    def getTeachingAssessPayload(self, token):
        """this function is totally XJTUic.
           once administrator change those value of checkboxes.
           we done.

        use it to do the ting teaching assessment.
        """
        if token.get('zbbm') is not None:
            token.pop('zbbm')
            if '实验' in self._soup.body.text:
                assessments = {1: 'PJDJ0643', 2: 'PJDJ0644', 3: 'PJDJ0627', 4: 'PJDJ0628', 5: 'PJDJ0629'}
                assessGrade = [1, 1, 1, 1, 1, 1, 1, 1, 2]
            else:
                assessments = {1: 'PJDJ0592', 2: 'PJDJ0593', 3: 'PJDJ0594', 4: 'PJDJ0605', 5: 'PJDJ0595'}
                assessGrade = [1, 1, 1, 1, 1, 1, 1, 1, 1, 2]
            token['ztpj'] = '老师认真负责'
            token['pgyj'] = '满意'
            token['sfytj'] = 'true'
            token['type'] = '2'
            token['actionType'] = '2'
            print(token)
            zbbm = []
            name = None
            assessIndex = -1
            for item in self._soup.find('table', id=True).find_all('input', attrs={'name': True, 'value': True}):
                if 'pfdj' in item.get('name') and item.get('name') != name:
                    name = item.get('name')
                    assessIndex += 1
                    token[name] = assessments[assessGrade[assessIndex]]
                if 'qz_' in item.get('name'):
                    token[item.get('name')] = '20'
                if 'zbbm' in item.get('name'):
                    zbbm.append(item.get('value'))
            payload = list(token.items())
            list(set(zbbm))
            for item in zbbm:
                payload.append(('zbbm', item))
            try:
                url = 'http://ssfw.xjtu.edu.cn/index.portal' + self._soup.find('form', action=True).get('action')
            except AttributeError as e:
                print(e)
                raise requests.HTTPError['NONONO']
            print(payload)
        return payload, url
