# 실행 전에 id.txt에 아이디와 비밀번호를 입력해 주세요
from selenium import webdriver
from urllib import parse
from bs4 import BeautifulSoup

last_name = "가,간,갈,감,강,개,경,계,고,곡,공,곽,교,구,국,군,궁,궉,권,기,근,금,길,김,나,난,남,내,노,뇌,누,단,담,당,대,도,돈,동,두,류,마,만,매,맹,명,모,묘,목,묵,문,미,민," \
            "박,반,방,배,백,변,범,복,봉,부,비,빈,빙,사,삼,상,서,석,선,설,섭,성,소,손,송,수,순,승,시,신,심,십,아,안,애,야,양,어,엄,여,연,염,엽,영,예,오,옥,온,옹,왕,요,용," \
            "우,운,원,위,유,육,윤,은,음,이,인,임,자,장,저,전,점,정,제,조,종,좌,주,준,즙,증,지,진,차,창,채,천,초,최,추,춘,탁,탄,태,판,팽,편,평,포,표,풍,피,필,하,학,한,함," \
            "해,허,현,호,홍,화,환,황,후,흥"

url = "https://go.sasa.hs.kr/autocomplete/get_hak2?term="
conti_check = False
student_list = [[] for _ in range(18)]
temp_student_list = [[] for _ in range(4)]

with open("id.txt", "r") as f:
    _id, _pw = f.readlines()

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

driver = webdriver.Chrome("chromedriver")

driver.implicitly_wait(3)
driver.get("https://go.sasa.hs.kr/auth")
driver.find_element_by_name('id').send_keys(_id)
driver.find_element_by_name('passwd').send_keys(_pw)
driver.find_element_by_xpath("/html/body/div/div[2]/form/div[3]/div[3]/input").click()

for last in last_name.split(','):
    driver.get(url + parse.quote(last))
    namelist = BeautifulSoup(driver.page_source, 'html.parser').text.split("\n")[-1][1:-1]  # 에러 회피
    last_check = last.encode('unicode_escape')
    last_check = last_check.decode('utf-8')
    if namelist != "":
        for name in namelist.split(","):
            if last_check == '\\' + name.split("\\")[1]:
                name = name[1:-1]
                _name = name.split(' ')[1]
                _name = _name.encode('utf-8')
                _name = _name.decode('unicode_escape')
                class_chr = name.split(' ')[0]
                if class_chr == "" or class_chr[2] == "0":  # 학번이 변경중인 경우
                    if class_chr == "":
                        temp_student_list[3].append(_name)
                    else:
                        temp_student_list[int(class_chr[0]) - 1].append(_name)
                    conti_check = True
                else:  # 학번이 정해진 경우
                    _grade = int(class_chr[0])
                    _class = int(class_chr[2])
                    student_list[_grade * 6 + _class - 7].append(_name)
                    temp_student_list[_grade - 1].append(_name)
driver.quit()

len_tuple = tuple(len(i) for i in temp_student_list)
print("전체 학생은 %d명입니다!" % sum(len_tuple))
if conti_check:
    print("반배정이 결정되지 않았습니다")
    print("1학년 : %d명\n2학년 : %d명\n3학년 : %d명\n졸업생 : %d명" % len_tuple)
    for i, li in enumerate(temp_student_list):
        print("-----------------------")
        if i == 3:
            print("졸업생")
        else:
            print("%d학년" % (i + 1))
        for st in li: print(st)
else:
    len_tuple = len_tuple[:-1]
    print("1학년 : %d명\n2학년 : %d명\n3학년 : %d명" % len_tuple)
    for i, li in enumerate(student_list):
        print("%d-%d" % (i / 6 + 1, i % 6 + 1))
        for j, st in enumerate(li):
            print("%d%d%02d %s" % (i / 6 + 1, i % 6 + 1, j + 1, st))
# 달빛학사 정보 얻기
# Code by Ryu
