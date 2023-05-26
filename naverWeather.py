import requests
from bs4 import BeautifulSoup
import os
import sys
import urllib.request
import json
import re

print("[간단한 지역 정보 조회 프로그램]")



class naverWeather():
    session = requests.Session()  
    addr = "https://weather.naver.com/today/"
    map_cityNum = {     # 지역 번호 매핑
        '가평': "02820250",'강화': "11710250",'고양': "02281621",'과천': "02290107",'광명': "02210610",'광주': "02610103",'구리': "02310541",'군포': "02410510",
        '김포': "02570106",'남양주': "02360103",'동두천': "02250510",'문산': "02480250",'부천': "02190108",'서울': "09140550",'성남': "02133101",'시흥': "02390630",
        '안산': "02273107",'안성': "02550510",'안양': "02171101",'양주': "02630510",'양평': "02830250",'여주': "02670510",'오산': "02370510",'용인': "02463102",
        '의왕': "02430101",'의정부': "0215020",'이천': "02500103",'인천': "11200510",'파주': "02480510",'평택': "02220630",'포천': "02650510",'하남': "02450530",
        '화성': "02590262",'백령도': "11720330",'연평도': "11720380",'양구': "01800250",'영월': "01750250",'원주': "01130115",'인제': "01810250",'정선': "01770250",
        '철원': "01780256",'춘천': "01110580",'평창': "01760250",'홍천': "01720250",'화천': "01790250",'횡성': "01730250",'강릉': "01150101",'강원': "01810350",
        '고성': "01820250",'대관령': "01760380",'동해': "01170101",'삼척': "01230106",'속초': "01210103",'양양': "01830250",'태백': "01190540",'괴산': "16760250",
        '남이': "15710360",'단양': "16800250",'보은': "16720250",'영동': "16740250",'옥천': "16730250",'음성': "16770250",'제천': "16150547",'증평': "16745250",
        '진천': "16750250",'청원': "16114101",'청주': "16111102",'추풍령': "16740335",'충주': "16130625",'계룡': "15250101",'공주': "15150102",'금산': "15710250",
        '논산': "15230109",'당진': "15270510",'대전': "07170630",'보령': "15180545",'부여': "15760250",'서산': "15210510",'서천': "15770253",'세종': "17110250",
        '아산': "15200600",'예산': "15810250",'천안': "15133253",'청양': "15790250",'태안': "15825250",'홍성': "15800250",'경산': "04290520",'경주': "04130126",
        '고령': "04830253",'구미': "04190110",'군위': "04720250",'김천': "04150575",'대구': "06110517",'문경': "04280610",'봉화': "04920250",'상주': "04250520",
        '성주': "04840250",'안동': "04170104",'영덕': "04770250",'영양': "04760250",'영주': "04210600",'영천': "04230520",'예천': "04900250",'울진': "04960250",
        '의성': "04730250",'청도': "04820250",'청송': "04750250",'칠곡': "04850250",'포항': "04113119",'거제': "03310109",'거창': "03880250",'고성': "03820250",
        '김해': "03250103",'남해': "03840250",'밀양': "03270103",'부산': "08470690",'사천': "03240330",'산청': "03860250",'서상': "03250102",'양산': "03330510",
        '울산': "10140510",'의령': "03720250",'진주': "03710119",'창녕': "03740250",'창원': "03129144",'통영': "03220111",'하동': "03850250",'함안': "03730250",
        '함양': "03870250",'합천': "03890250",'독도': "04940250",'울릉도': "04940250",'고창': "13790250",'군산': "13130134",'김제': "13210107",'남원': "13190116",
        '무주': "13730250",'부안': "13800250",'순창': "13770250",'완주': "13710360",'익산': "13140113",'임실': "13750250",'장수': "13740250",'전주': "13113102",
        '강진': "12810250",'고흥': "12770250",'곡성': "12720250",'광양': "12230530",'광주': "05140120",'구례': "12730250",'나주': "12170102",'담양': "12710250",
        '목포': "12110510",'무안': "12840250",'보성': "12780250",'순천': "12150119",'신안': "12910253",'여수': "12130780",'영광': "12870250",'영암': "12830250",
        '완도': "12890250",'장성': "12880250",'장흥': "12800250",'진도': "12900250",'함평': "12860250",'해남': "12820250",'화순': "12790250",'흑산도': "12910360",
        '서귀포': "14130590",'제주': "14110104"
            
            }

    def __init__(self, area):
        
        
        self.area = area
        self.addr = None
        self.result = None
        
        if area in naverWeather.map_cityNum:
            cityNum = naverWeather.map_cityNum[area]
        else:
            print("옳지않은 지역명입니다. 다시입력해주세요")
            return main()
        

        self.addr = naverWeather.addr + cityNum
        
        self.search()

    def search(self):
        naverWeather.session.encoding = 'utf-8'

        request = naverWeather.session.get(self.addr)
        soup = BeautifulSoup(request.text, "html.parser")
        table = soup.find(class_="week_list")
        
        t_ary = list(table.stripped_strings)

        self.result =("[" + self.area +"의" ""+" 날씨]\n"
                    + "- 오늘(" + t_ary[1] +")\n"
                    + " \t 오전 - " + t_ary[11][:-1] + "℃ (" + t_ary[5] + ", 강수확률 : " + t_ary[4] + ")\n"
                    + " \t 오후 - " + t_ary[14][:-1] + "℃ (" + t_ary[6] + ", 강수확률 : " + t_ary[9] + ")\n"
                    + "- 내일(" + t_ary[16] + ")\n"
                    + " \t 오전 - " + t_ary[26][:-1] + "℃ (" + t_ary[20] + ", 강수확률 : " + t_ary[19] + ")\n"
                    + " \t 오후 - " + t_ary[29][:-1] + "℃ (" + t_ary[21] + ", 강수확률 : " + t_ary[24] + ")\n")



    def getWeather(self):
       
        return self.result

        
def display_menu():
    print("메뉴를 선택하세요:")
    print("1.관광지")
    print("2.맛집")
    print("3.펜션")
    print("4.다른지역검색")
    print("5.종료")
    

def main():
    city = input("지역이름을 입력해주세요: ")    
    temp = naverWeather(city)
    print(temp.getWeather())
    area_url="https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query="
    search_url=area_url+city
    r= requests.get(search_url)
    soup=BeautifulSoup(r.text,"html.parser")
    a=soup.select(".desc-YyCP9")
    try:
            print(a[0].text)
            print()
    except ValueError:
            pass 
    except IndexError:
            pass


    while True:
        display_menu()  
        option = int(input("선택할 옵션의 번호를 입력하세요: "))  
        client_id = "VbT2fYWoyz09OkGzSC5v"
        client_secret = "kZ6yj5Wvfa"

        if option == 1:
            encText = urllib.parse.quote(city+"관광지")
            url = "https://openapi.naver.com/v1/search/local?query=" + encText +'&display=5' 
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id",client_id)
            request.add_header("X-Naver-Client-Secret",client_secret)
            response = urllib.request.urlopen(request)
            rescode = response.getcode()

            if(rescode==200):
             response_body = response.read()
             data=json.loads(response_body.decode('utf-8'))
             for item in data['items']:
                remove_tag=re.compile('<.*?>')
                title = re.sub(remove_tag,'',item['title'])
                category =re.sub(remove_tag,'',item['category'])
                address = re.sub(remove_tag,'',item['address'])
                print()
                print("Title:", title)
                print("Category:", category)
                print("Address:", address)
                print()
            else:
             print("Error Code:" + rescode)
        
        elif option == 2:
            encText = urllib.parse.quote(city+"맛집")
            url = "https://openapi.naver.com/v1/search/local?query=" + encText +'&display=5' 
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id",client_id)
            request.add_header("X-Naver-Client-Secret",client_secret)
            response = urllib.request.urlopen(request)
            rescode = response.getcode()

            if(rescode==200):
             response_body = response.read()
             data=json.loads(response_body.decode('utf-8'))
             for item in data['items']:
                remove_tag=re.compile('<.*?>')
                title = re.sub(remove_tag,'',item['title'])
                category =re.sub(remove_tag,'',item['category'])
                address = re.sub(remove_tag,'',item['address'])
                print()
                print("Title:", title)
                print("Category:", category)
                print("Address:", address)
                print()
            else:
             print("Error Code:" + rescode)

        elif option == 3:
            encText = urllib.parse.quote(city+"펜션")
            url = "https://openapi.naver.com/v1/search/local?query=" + encText +'&display=5' + '&sort=comment' 
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id",client_id)
            request.add_header("X-Naver-Client-Secret",client_secret)
            response = urllib.request.urlopen(request)
            rescode = response.getcode()

            if(rescode==200):
             response_body = response.read()
             data=json.loads(response_body.decode('utf-8'))
             for item in data['items']:
                remove_tag=re.compile('<.*?>')
                title = re.sub(remove_tag,'',item['title'])
                link =re.sub(remove_tag,'',item['link'])
                address = re.sub(remove_tag,'',item['address'])
                print()
                print("Title:", title)
                print("link:", link)
                print("Address:", address)
                print()
            else:
             print("Error Code:" + rescode)
        
        elif option == 4:
            main()
        elif option == 5:
            print("프로그램을 종료합니다.")     
        else:
            print("올바른 옵션을 선택해주세요.")
        if option == 5:
              break
           
              
    

if __name__ == "__main__":
    main()

    
    

