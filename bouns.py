# 실행 전에 id.txt에 아이디와 비밀번호를 입력해 주세요
from selenium import webdriver
from bs4 import BeautifulSoup

url = "https://go.sasa.hs.kr/autocomplete/get_hak2?term"
conti_check = False
student_list = [[] for _ in range(18)]
temp_student_list = [[] for _ in range(4)]

with open("id.txt", "r") as f:
    _id, _pw = f.readlines()

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument('disable-gpu')

driver = webdriver.Chrome("chromedriver", options=options)

driver.implicitly_wait(3)
driver.get("https://go.sasa.hs.kr/auth")
driver.find_element_by_name('id').send_keys(_id)
driver.find_element_by_name('passwd').send_keys(_pw)
driver.find_element_by_xpath("/html/body/div/div[2]/form/div[3]/div[3]/input").click()
driver.get(url)
namelist = BeautifulSoup(driver.page_source, 'html.parser').text.split("\n")[-1][1:-1]  # 에러 회피
for name in namelist.split(","):
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
    print("1학년 : %d명\n2학년 : %d명\n3학년 : %d명" % len_tuple[:-1])
    for i, li in enumerate(student_list):
        print("%d-%d" % (i / 6 + 1, i % 6 + 1))
        for j, st in enumerate(li):
            print("%d%d%02d %s" % (i / 6 + 1, i % 6 + 1, j + 1, st))
# 달빛학사 정보 얻기
# Code by Ryu
