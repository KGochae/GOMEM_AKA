
import re
import streamlit as st
import numpy as np
import pandas as pd
import requests
import pickle
import isodate
import tqdm

import warnings
warnings.filterwarnings("ignore")

from collections import Counter
from PIL import Image, ImageDraw

# ------------------------------------------------------------------------------------------------------------------------------------------- #


# 댓글의 키워드 분석
word_rules = {
    # "우왁굳" : ['왁굳','영택','오영택','우왁굳','왁굳형'],
    "뢴트게늄" : ['뢴트게늄','뢴트','초코푸딩'],
    "해루석" : ['루숙','해루석','해루숙','루석'],
    "캘리칼리": ['캘칼', '캘리칼리', '캘리칼리데이빈슨'],
    "도파민" :['도파민','파민','박사'],
    "소피아" : ['소피아','춘피아'],
    "권민" : ['권민','쿤미옌'],
    "왁파고": ['왁파고', '파고', '황파고'],
    "독고혜지": ['혜지','독고혜지'],
    "비밀소녀": ['비소','비밀소녀','비밀이모'],
    "히키킹" : ['히키킹','히키퀸','히키킹구'],
    "곽춘식" : ['춘식','곽춘식','춘피아'],
    "김치만두" : ['만두','김치만두번영택사스가','김치만두','만두'],
    "하쿠" : ['하쿠','미츠네 하쿠'],
    "비즈니스킴":['비킴','비즈니스킴'],
    "풍신" :['풍신'],
    "프리터":['프리터'],
    "단답벌레" : ['단답벌레','단답'],
    "융터르" : ['카르나르','융털','융터르'],
    "호드" : ['호드','노스페라투스'],
    "이덕수" : ['덕수','이덕수'],

    "미미짱짱세용" : ['미미짱짱세용','세용'],
    "닌닌" : ['닌닌','긱긱'],
    "젠투" : ['젠투','젠크리트'],
    "수셈이" : ['셈이','수셈이'],
    "아마최" : ['아마데우스최','아마최'],
    "진희" : ['진희','지니'],
    "수셈이": ['셈이','수셈이'],
    "발렌타인" : ['발렌','발렌타인','미발'],
    "시리안": ['시리안'],
    "길버트":['길버트'],
    "빅토리":['빅토리'],

    "이세돌" :['이세돌','세돌','이세계아이돌'],
    "아이네" : ['아이네','아잉네','햄이네'],
    "징버거" : ['징버거','버거','버거땅'],
    "릴파" : ['릴파'],
    "주르르" : ['르르땅','주르르','르르'],
    "고세구" : ['고세구','세구땅','세구','눈나구','막내즈'],
    "비챤" : ['챠니','챤이','비챤','막내즈']
}



def wordCount(comment_df):
    all_tmp = [word for sublist in comment_df['tmp'] for word in sublist] # word = 리스트 속 ['단어들']
 
#   통일된 단어들만 추출
    unified_words = []
    for word in all_tmp:
        for unified_word, variations in word_rules.items():
            if word in variations:
                unified_words.append(unified_word)
                break
 
    unified_tmp = Counter(unified_words)
    most_common_words = unified_tmp.most_common(10)

    return most_common_words


def get_member_images(top_members):

    member_images = {}
    for i, member in enumerate(top_members):
        name = member[0]
        image_path = f"img/{name}.jpg"  # 이미지 파일 이름 생성 
        img = Image.open(image_path).convert("RGBA")

        # 원형으로 크롭
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + img.size, fill=255)
        img.putalpha(mask)

        # 크기 조절
        img = img.resize((80, 80))

        member_images[name] = img

    return member_images




# 단어를 통일시키는 함수
def unify_word(word, gomem_word):
    for unified_word, variations in gomem_word.items():
        if word in variations:
            return unified_word
    return word

def unify_tmp(tmp, gomem_word):
    return [unify_word(word, gomem_word) for word in tmp] # tmp 에 있는 word 들을 



# 월별 고멤 언급량
def gomem_comment(df, col, year, month):
    if month == 'all':
        df = df[df['year'] == year]
    else:
        df = df[(df['year'] == year) & (df['month'] == month)]

    all_tmp = [word for sublist in df[col] for word in sublist] # word = 리스트 속 ['단어들']
    gomem_word = {
        "뢴트게늄" : ['뢴트게늄','뢴트','초코푸딩'],
        "해루석" : ['루숙','해루석','해루숙','루석'],
        "캘리칼리": ['캘칼', '캘리칼리', '캘리칼리데이빈슨'],
        "도파민" :['도파민','파민','박사','할배즈'],
        "소피아" : ['소피아','춘피아'],
        "권민" : ['권민','쿤미옌'],
        "왁파고": ['왁파고', '파고', '황파고'],
        "독고혜지": ['혜지','독고혜지'],
        "비밀소녀": ['비소','비밀소녀','비밀이모'],
        "히키킹" : ['히키킹','히키퀸'],
        "곽춘식" : ['춘식','곽춘식','춘피아'],
        "김치만두" : ['김치만두','만두','김치만두번영택사스가'],
        "하쿠" : ['하쿠','미츠네 하쿠'],
        "비즈니스킴":['비킴','비즈니스킴'],
        "풍신" :['풍신','할배즈'],
        "프리터":['프리터'],
        "단답벌레" : ['단답벌레','단답'],
        "융터르" : ['카르나르','융털','융터르'],
        "호드" : ['호드','노스페라투스'],
        "이덕수" : ['덕수','이덕수','할배즈'],
    }

    aka_word = {
        "미미짱짱세용" : ['미미짱짱세용','세용'],
        "닌닌" : ['닌닌'],
        "젠투" : ['젠투','젠크리트'],
        "수셈이" : ['셈이','수셈이'],
        "아마최" : ['아마데우스최','아마최'],
        "진희" : ['진희','지니'],
        "수셈이": ['셈이','수셈이'],
        "발렌타인" : ['발렌','발렌타인','미발'],
        "시리안": ['시리안'],
        "길버트":['길버트'],
        "빅토리":['빅토리','맑눈광','토리'],
        "설리반":['설리반']
    }

    # 통일된 단어들만 추출 (gomem_word에 있는 단어들만 포함)

    # gomem_word와 aka_word에 속하는 단어들을 추출
    unified_tmp_gomem = unify_tmp(all_tmp, gomem_word)
    unified_tmp_gomem = [word for word in unified_tmp_gomem if word in gomem_word]
    
    unified_tmp_aka = unify_tmp(all_tmp, aka_word)
    unified_tmp_aka = [word for word in unified_tmp_aka if word in aka_word]
    
    # 각각의 단어 리스트를 Counter로 변환하여 가장 많이 나오는 단어들을 추출
    most_gomem = Counter(unified_tmp_gomem).most_common(5)
    most_aka = Counter(unified_tmp_aka).most_common(5)

    return  most_gomem, most_aka


# 최종 실행함수

def monthly_gomem(df):
  # 월별로 데이터를 계산하고 저장할 딕셔너리를 초기화합니다.
    gomem_chart = {}

  # 각 월별 데이터 계산 및 저장
    for month in range(1, 12):
        most_gomem, most_aka = gomem_comment(df, 'tmp', 2023, month)
        most_common_words = most_gomem + most_aka
        month_data = [{'id': gomem_name, 'count': count} for gomem_name, count in most_common_words]
        gomem_chart[month] = month_data

  # 고멤 이름을 추출합니다.(중복x)
    member_names = set(item['id'] for month_data in gomem_chart.values() for item in month_data)

  # 결과를 담을 리스트를 초기화합니다.
    result = []

    # 각 고멤에 대한 데이터를 생성합니다.
    for member_name in member_names:
        member_data = {
            "id": member_name,
            "data": []
        }
        for month, month_data in gomem_chart.items():
            month_count = next((item['count'] for item in month_data if item['id'] == member_name), 0)
            member_data['data'].append({
                "x": month,
                "y": month_count
            })
        
        result.append(member_data)

    return result


def count_word(word_list, target_word):
    return word_list.count(target_word)


# 최종 실행함수 원하는 '고멤' 언급이 많은 video_id 찾기
def gomem_video(df, gomem):  
  
  # 단어통일
  df['tmp'] = df['tmp'].apply(lambda x: unify_tmp(x, word_rules))
  # '고멤' 단어가 언급된 빈도를 계산하여 데이터프레임에 추가
  df['cnt'] = df['tmp'].apply(lambda x: count_word(x, gomem))
  df = df.groupby(['video_id','title'])['cnt'].sum().reset_index()
  gomem_hot_video = df[df['cnt'] == df['cnt']].nlargest(6,'cnt')[['video_id','title','cnt']]

  # 결과 출력
  return gomem_hot_video



