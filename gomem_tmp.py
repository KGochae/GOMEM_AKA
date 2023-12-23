import streamlit as st
import pandas as pd
import ast 

from streamlit_elements import dashboard
from streamlit_elements import nivo, elements, mui
from NLP import  get_member_images, gomem_video, gomem_comment, monthly_gomem



 # --------------------------------------------------------------고멤 TOP 5 -----------------------------------------------------------------------------------------  #
with open( "font.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
pd.set_option('mode.chained_assignment',  None)

@st.cache_data
def get_comment():
    comment_data = pd.read_csv('csv/gomem_tmp_20231130.csv')
    comment_data['tmp'] = comment_data['tmp'].apply(ast.literal_eval)
    return comment_data

with st.spinner('댓글 가져오는 중..👀'):
    comment_data = get_comment()



st.header('WAKTAVERSE 📊')

st.markdown(''' 
            > * (2023.01 ~ 2023.11.30) 본채널과 왁타버스 채널에 올라온 :green[고정멤버 편집영상(예능)]의 시청자 댓글을 수집하여 언급량을 정리해보았습니다. 
            > * 커버곡, 돚거 클립은 제외 했기 때문에 편차가 있습니다. 재미로만 참고해주시면 감사하겠습니다🤤
            ''')

st.divider()


if comment_data is not None:
    if hasattr(st.session_state, 'comment_data'):
        comment_data = st.session_state.comment_data

    else:         
        comment_data = comment_data[comment_data['year'] == 2023]
        nivo_gomem = monthly_gomem(comment_data)
        comment_data = comment_data.groupby(['video_id','title','year','month'])['tmp'].sum().reset_index()

        st.session_state.comment_data = comment_data 
        st.session_state.nivo_gomem = nivo_gomem

        
    with st.container():
        col1,col2 = st.columns([1.2,2])
        with col1:
            st.subheader('🤡 월별 고정멤버 언급량 TOP5 ')
            st.caption('올해 고정멤버 언급량 top5를 확인해보세요! (시청자가 댓글을 작성한 날짜 기준으로 집계)')
            
            with st.form(key="waktaverse_aka_comment"):
                c1,c2,c3 = st.columns([1,4,1])       

                with c1:
                    month_option = st.selectbox('month',[11,10,9,8,7,6,5,4,3,2,1,'all'], key='gomem_month')
                    most_gomem, most_aka = gomem_comment(comment_data,'tmp', 2023, month_option)                    

                    st.session_state.most_gomem = most_gomem
                    st.session_state.most_aka = most_aka

                with c2:
                    if hasattr(st.session_state, 'most_gomem'):
                        most_gomem = st.session_state.most_gomem
                    if hasattr(st.session_state, 'most_aka'):
                        most_aka = st.session_state.most_aka

                    gomem_aka = st.selectbox('month',['고정멤버','아카데미'], key='gomem_aka')
                    
                    if gomem_aka == '고정멤버':
                        gomem_aka = most_gomem
                        gomem = [item[0] for item in gomem_aka]

                    elif gomem_aka == '아카데미':
                        gomem_aka = most_aka
                        gomem = [item[0] for item in gomem_aka]

                with c3:                    
                    gomem_img = get_member_images(gomem_aka)                        
                    st.session_state.gomem_img = gomem_img                        
                    submit_search = st.form_submit_button("확인")


                if hasattr(st.session_state, 'gomem_img'):
                    gomem_img = st.session_state.gomem_img
                    if month_option == 'all':
                        caption = f'2023년 ":green[왁타버스(예능)]" 영상에서 가장 언급이 많았던 멤버입니다.'
                    else:
                        caption = f'{month_option}월 ":green[왁타버스(예능)]" 영상에서 가장 언급이 많았던 멤버입니다.'
                        
                    st.caption(caption)



                    # st.caption(f'{month_option}월 ":green[왁타버스(예능)]" 영상에서 가장 반응이 뜨거웠던 (언급이 많았던) 멤버입니다.')

                    try:
                        for i, member in enumerate(gomem_aka):
                            name = member[0]
                            img = gomem_img[name]
                    
                        if img:                       
                            with st.container():
                                c1,c2,c3,c4,c5 = st.columns([1,1,1,1,1]) 
                                with c1:
                                    if len(gomem) > 0 :
                                        st.image(gomem_img[gomem_aka[0][0]], width=80)
                                        st.metric('hide',f'🥇{gomem_aka[0][0]}',f'{gomem_aka[0][1]}')

                                with c2:
                                    if len(gomem) > 1 :
                                        st.image(gomem_img[gomem_aka[1][0]], width=80)
                                        st.metric('hide',f'{gomem_aka[1][0]}',f'{gomem_aka[1][1]}')
                                
                                with c3:
                                    if len(gomem) > 2 :
                                        st.image(gomem_img[gomem_aka[2][0]], width=80)
                                        st.metric('hide',f'{gomem_aka[2][0]}',f'{gomem_aka[2][1]}')
                                
                                with c4:
                                    if len(gomem) > 3 :
                                        st.image(gomem_img[gomem_aka[3][0]], width=80)
                                        st.metric('hide',f'{gomem_aka[3][0]}',f'{gomem_aka[3][1]}')
                                
                                with c5:
                                    if len(gomem) > 4 :
                                        st.image(gomem_img[gomem_aka[4][0]], width=80)
                                        st.metric('hide',f'{gomem_aka[4][0]}',f'{gomem_aka[4][1]}')

                    except KeyError:
                            st.write('error')

            if hasattr(st.session_state, 'nivo_gomem'):
                nivo_gomem = st.session_state.nivo_gomem
                gomem_option = st.selectbox('gomem', gomem, key='gomem_name')
                gomem_hot_video = gomem_video(comment_data, gomem_option) 
                filter_data = [item for item in nivo_gomem if item['id'] in gomem_option]
                

            with elements("gomem_nivo"):
                layout=[            
                    dashboard.Item("item_1", 0, 0, 5, 1.5)
                    ]
                with dashboard.Grid(layout):

                    mui.Box( # 월별 언급량
                        children =[
                            mui.Typography(f' (2023) {gomem_option} 월별 언급량',
                                        variant="body2",
                                        color="text.secondary",sx={"text-align":"left","font-size":"14px"}),

                            nivo.Line(
                            data= filter_data,
                            margin={'top': 20, 'right': 30, 'bottom': 30, 'left': 40},
                            xScale={'type': 'point',
                                    },

                            curve="cardinal",
                            axisTop=None,
                            axisRight=None,
                            axisBottom=True,

                            # axisLeft={
                            #     'tickSize': 4,
                            #     'tickPadding': 10,
                            #     'tickRotation': 0,
                            #     'legend': '조회수',
                            #     'legendOffset': -70,
                            #     'legendPosition': 'middle'
                            # },
                            colors= {'scheme': 'accent'},
                            enableGridX = False,
                            enableGridY = False,
                            enableArea = True,
                            areaOpacity = 0.3,
                            lineWidth=2,
                            pointSize=5,
                            pointColor='white',
                            pointBorderWidth=0.5,
                            pointBorderColor={'from': 'serieColor'},
                            pointLabelYOffset=-12,
                            useMesh=True,
                            legends=[
                                        {
                                        'anchor': 'top-left',
                                        'direction': 'column',
                                        'justify': False,
                                        # 'translateX': -30,
                                        # 'translateY': -200,
                                        'itemsSpacing': 0,
                                        'itemDirection': 'left-to-right',
                                        'itemWidth': 80,
                                        'itemHeight': 15,
                                        'itemOpacity': 0.75,
                                        'symbolSize': 12,
                                        'symbolShape': 'circle',
                                        'symbolBorderColor': 'rgba(0, 0, 0, .5)',
                                        'effects': [
                                                {
                                                'on': 'hover',
                                                'style': {
                                                    'itemBackground': 'rgba(0, 0, 0, .03)',
                                                    'itemOpacity': 1
                                                    }
                                                }
                                            ]
                                        }
                                    ],                            
                            theme={
                                    # "background-color": "rgba(158, 60, 74, 0.2)",
                                    "textColor": "white",
                                    "tooltip": {
                                        "container": {
                                            "background": "#3a3c4a",
                                            "color": "white",
                                        }
                                    }
                                },
                            animate= True)
                            
                            ] ,key="item_1")


        with col2:
            st.markdown(f''' 
                        ### {gomem_option} 영상 더보기
                        *  :green[{gomem_option}]의 :green[언급량]이 많은 대표 영상 TOP6 입니다!  ''' )

            hot_video_card_sx = { #  타이틀 조회수증가량 css
                                "display": "flex",
                                "item-align":"center",
                                "gap":"10px",
                                "justify-content":"center",
                                "height": "50px",
                                "width" : "240px",
                                "padding-bottom": "5px", 
                                "padding-top": "5px",  
                                }

            title_sx = {"font-size":"12px",
                        "align-self": "center",
                        "max-height": "100%",
                        "overflow": "hidden",
                        "width" : "160px",
                        "item-align":"center",
                        # "fontFamily":"Pretendard Variable"                                            
                        }   
            with elements("gomem_hot_video"):
                    layout=[
                
                        dashboard.Item(f"item_0", 0, 0, 2, 1.5, isDraggable=False, isResizable=False  ), #isDraggable=False, isResizable=True                    
                        dashboard.Item(f"item_1", 2, 0, 2, 1.5, isDraggable=False, isResizable=False ),                    
                        dashboard.Item(f"item_2", 4, 0, 2, 1.5, isDraggable=False, isResizable=False ),                    
                        dashboard.Item(f"item_3", 0, 2, 2, 1.5, isDraggable=False, isResizable=False ),                    
                        dashboard.Item(f"item_4", 2, 4, 2, 1.5, isDraggable=False, isResizable=False ),                    
                        dashboard.Item(f"item_5", 4, 0, 2, 1.5, isDraggable=False, isResizable=False ),                    

                        ]
                    with dashboard.Grid(layout):
                        for i in range(6):
                            mui.Box(
                                    mui.CardContent( # 재생목록/링크
                                        sx={'display':'flex',
                                            'padding': '2px 0 0 0'
                                            },
                                        children=[
                                            mui.Typography(
                                                        f"{gomem_option} 추천 영상",
                                                        component="div",
                                                        sx={"font-size":"12px",
                                                            "padding-left": 10,
                                                            "padding-right": 10}                            
                                                    ),
                                            mui.Link(
                                                "🔗",
                                                href=f"https://www.youtube.com/watch?v={gomem_hot_video['video_id'].iloc[i]}",
                                                target="_blank",
                                                sx={"font-size": "12px",
                                                    "font-weight": "bold"}
                                                    )                                                                                       
                                                ]                            
                                            ),


                                    mui.CardMedia( # 썸네일 이미지
                                        sx={ "height": 150,
                                            "backgroundImage": f"linear-gradient(rgba(0, 0, 0, 0), rgba(0,0,0,0.5)), url(https://i.ytimg.com/vi/{gomem_hot_video['video_id'].iloc[i]}/sddefault.jpg)",
                                            # "mt": 0.5
                                            },
                                        ),

                                    mui.CardContent( # 타이틀 조회수증가량
                                        sx = hot_video_card_sx,
                                        children=[
                                            mui.Typography( # 타이틀
                                                f"{gomem_hot_video['title'].iloc[i]}",
                                                component="div",
                                                sx=title_sx                           
                                            ),
                                        
                                            mui.Divider(orientation="vertical",sx={"border-width":"1px"}), # divider 추가
                                        
                                            mui.Box(
                                                sx={"align-items": "center"},
                                                children = [
                                                    mui.Typography(
                                                        f"{int(gomem_hot_video['cnt'].iloc[i])}",
                                                            variant='body2', 
                                                        sx={
                                                            "font-size" : "25px",
                                                            "fontWeight":"bold",
                                                            "text-align":"center",
                                                            "height":"30px"
                                                            },     
                                                        ),   
                                                    mui.Typography(
                                                        "언급량",
                                                            variant='body2', 
                                                        sx={
                                                            "font-size" : "10px",
                                                            "fontWeight":"bold",
                                                            "text-align":"center"
                                                            },     
                                                        )
                                                    ]                                                        
                                                ),
                                            ]
                                        )                       
                                            ,key=f'item_{i}',sx={"borderRadius": '23px'})



st.divider()

# json_filename = os.path.expanduser("C:/scraping/csv_data/nivo_gomem_data.json")
# with open(json_filename, "w") as json_file:
#     json.dump(nivo_gomem, json_file)

