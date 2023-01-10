import re 
import requests
import os
# import json

url_tab_rows = "https://ssuz.vip.edu35.ru/actions/register/lessons_tab/lessons_tab_rows"
url_save = "https://ssuz.vip.edu35.ru/actions/register/lessons_tab/lessons_tab_save_work_lesson_subject"
url_close = "https://ssuz.vip.edu35.ru/actions/register/lessons_tab/lessons_tab_close_lesson_action"
url_open = "https://ssuz.vip.edu35.ru/actions/register/lessons_tab/lessons_tab_open_lesson_action"

dates = '05.01.2023'
cookie = 'ssuz_sessionid=9xfegg7mz20luln4quk0iy217om4b90a'


name = ''
les_id = 0

spisok = [
    {"group": "питпм_исп221а", "student_id": 70002, "group_id": 4649,"subject_id":"6132", "id":0},#0
    {"group": "питпм_исп221ав", "student_id": 70027, "group_id": 4659,"subject_id":"6132", "id":1},#1
    {"group": "рмп_исп320а", "student_id": 61655, "group_id": 4078,"subject_id":"6133", "id":2},#2
    {"group": "рмп_исп320ав", "student_id": 61683, "group_id": 4079,"subject_id":"6133", "id":3},#3
    {"group": "питпм_исп320п", "student_id": 61684, "group_id": 4080,"subject_id":"6132", "id":4},#4
    {"group": "питпм_исп320пв", "student_id": 61709, "group_id": 4081,"subject_id":"6132", "id":5},#5
    {"group": "ркис_исп320р", "student_id": 61712, "group_id": 4086,"subject_id":"6189", "id":6},#6
    {"group": "ркис_исп320рв", "student_id": 61680, "group_id": 4087,"subject_id":"6189", "id":7},#8
    {"group": "тис_исп320р", "student_id": 61712, "group_id": 4086,"subject_id":"6190", "id":8},#7
    {"group": "тис_исп320рв", "student_id": 61680, "group_id": 4087,"subject_id":"6190", "id":9},#9
    {"group": "опбд_сис221", "student_id": 69973, "group_id": 4644,"subject_id":"5548", "id":10},#10
    {"group": "опбд_сис221в", "student_id": 69998, "group_id": 4653,"subject_id":"5548", "id":11},#11
    {"group": "обвп_исп419р", "student_id": 48698, "group_id": 2848,"subject_id":"8010", "id":12},#12
    {"group": "обвп_исп419рв", "student_id": 49324, "group_id": 2945,"subject_id":"8010", "id":13},#13
]

spisok_practicy = [
    {"group": "питпм_исп221а", "student_id": '70016', "group_id": '4649',"subject_id":'6132',"sub_group_id":'13664', "id":0},#1
    {"group": "питпм_исп221ав", "student_id": '70016', "group_id": '4649',"subject_id":'6132',"sub_group_id":'13665', "id":1},#2
    {"group": "питпм_исп221ав", "student_id": '70027', "group_id": '4659',"subject_id":'6132', "id":2},

    {"group": "рмп_исп320а", "student_id": '61655', "group_id": '4078',"subject_id":"6133","sub_group_id":'12601', "id":3},
    {"group": "рмп_исп320ав", "student_id": '61655', "group_id": '4078',"subject_id":"6133","sub_group_id":'12602', "id":4},
    {"group": "рмп_исп320ав", "student_id": '61683', "group_id": '4079',"subject_id":"6133", "id":5},

    {"group": "питпм_исп320п", "student_id": '61684', "group_id": '4080',"subject_id":"6132","sub_group_id":'12640', "id":6},
    {"group": "питпм_исп320пв", "student_id": '61684', "group_id": '4080',"subject_id":"6132","sub_group_id":'12641', "id":7},
    {"group": "питпм_исп320пв", "student_id": '61709', "group_id": '4081',"subject_id":"6132", "id":8},

    {"group": "ркис_исп320р", "student_id": '61712', "group_id": '4086',"subject_id":"6189","sub_group_id":'11776', "id":9},
    {"group": "ркис_исп320рв", "student_id": '61712', "group_id": '4086',"subject_id":"6189","sub_group_id":'11777', "id":10},
    {"group": "ркис_исп320рв", "student_id": '61680', "group_id": '4087',"subject_id":"6189", "id":11},

    {"group": "тис_исп320р", "student_id": '61712', "group_id": '4086',"subject_id":"6190","sub_group_id":'12654', "id":12},
    {"group": "тис_исп320рв", "student_id": '61712', "group_id": '4086',"subject_id":"6190","sub_group_id":'12655', "id":13},
    {"group": "тис_исп320рв", "student_id": '61680', "group_id": '4087',"subject_id":"6190", "id":14},

    {"group": "опбд_сис221", "student_id": '69973', "group_id": '4644',"subject_id":"5548","sub_group_id":'13640', "id":15},
    {"group": "опбд_сис221в", "student_id": '69973', "group_id": '4644',"subject_id":"5548","sub_group_id":'13641', "id":16},
    {"group": "опбд_сис221в", "student_id": '69998', "group_id": '4653',"subject_id":"5548", "sub_group_id":'13641',"id":17},

    {"group": "обвп_исп419р", "student_id": '48698', "group_id": '2848',"subject_id":"8010","sub_group_id":'13379', "id":18},
    {"group": "обвп_исп419рв", "student_id": '48698', "group_id": '2848',"subject_id":"8010","sub_group_id":'13380', "id":19},
    {"group": "обвп_исп419рв", "student_id": '49324', "group_id": '2945',"subject_id":"8010", "id":20},
]

headers = {
    'Host': 'ssuz.vip.edu35.ru',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': cookie
}

def payload_rows_teory(dates,group_id,subject_id):
  payload = {
    "unit_id": 22,
    "period_id":	30,
    "date_from":	"2022-09-01T00:00:00",
    "date_to":	dates,
    "practical":	"",
    "slave_mode":	"1",
    "month":	"",
    "group_id":	group_id,
    "subject":	"0",
    "subject_gen_pr_id":	"0",
    "exam_subject_id":	"0",
    "subject_sub_group_obj":	"{\"subject_id\": "+subject_id+"}",
    "subject_id":	subject_id,
    "view_lessons":	"false"
  }
  return payload

def payload_rows_practicy(dates,group_id,subject_id,sub_group_id):
  payload = {
    "unit_id": 22,
    "period_id":	30,
    "date_from":	"2022-09-01T00:00:00",
    "date_to":	dates,
    "practical":	"1",
    "slave_mode":	"1",
    "month":	"",
    "group_id":	group_id,
    "subject":	"0",
    "subject_gen_pr_id":	"0",
    "exam_subject_id":	"0",
    "subject_sub_group_obj": "",
    "subject_id":	subject_id,
    # "view_lessons":	"false"
  }
  if sub_group_id==0:
    payload["subject_sub_group_obj"] = "{\"subject_id\": "+subject_id+"}"
  else:
    payload["subject_sub_group_obj"] = "{\"subject_id\": "+subject_id+", \"sub_group_id\": "+sub_group_id+"}"
  return payload

def payload_rows_practicy_save_tema(les_id,student_id,dates,group_id,subject_id,sub_group_id,name_lessons):
  payload =  {
              "lesson_id": les_id,
              "student_id": student_id,
              "unit_id": "22",
              "period_id": "30",
              "date_from": "2022-09-01T00:00:00",
              "date_to": dates,
              "practical": "1",
              "slave_mode": "1",
              "month": "",
              "group_id": group_id,
              "subject": "0",
              "subject_gen_pr_id": "0",
              "exam_subject_id": "0",
              "subject_sub_group_obj":	"",#{\"subject_id\": "+name['subject_id']+"}",
              "subject_id": subject_id,
              "view_lessons": "false",
              "lesson_subject": name_lessons
              }
  if sub_group_id==0:
    payload["subject_sub_group_obj"] = "{\"subject_id\": "+subject_id+"}"
  else:
    payload["subject_sub_group_obj"] = "{\"subject_id\": "+subject_id+", \"sub_group_id\": "+sub_group_id+"}"
  return payload

def createFile(diir):
  for name in spisok:
        try:
          with open(diir+"\\"+name['group']+'.txt','w',encoding="utf-8") as file2:
            print(name['group'])
        except Exception as e:
          print(e)
        finally:
          file2.close()

def dubleFileAll(diir,ch2,ch21):
  # spisok1 = ''
  if ch2==1:
    diir = diir+'\\лекции'
    spisok1 = [spisok[ch21]]

  elif ch2==2:
    diir = diir+'\\практика'
    spisok1 = [spisok_practicy[ch21]]

  else:
    print('Такого действия нет')
  spisok1 = spisok

  for name in spisok1:
    data_list= []
    with open(diir+"\\"+name['group']+'.txt',encoding="utf-8") as file:
      try:
        lines = file.readlines()
        for i in lines:
          text =i.rstrip() 
          match = re.findall('[1-9]', text)
          # print(match)
          match = match[-1] if match else 0
          for c in range(int(match)):
            text=text.replace(match, "") 
            data_list.append(text.rstrip())

      except Exception as e:
        print(e)

      finally:
      # print(spisok)
        file.close()


    try:
      with open(diir+"\\rasp_"+name['group']+'.txt','w',encoding="utf-8") as file2:
        # file2.write("\n".join(spisok).join("\n"));
        for item in data_list:
          file2.write("%s\n" % item)
          

    except Exception as e:
      print(e)

    finally:
      # print(name['group'],'Готово')
      file2.close()

def saveThemesPracticy(diir,ch31):
  if ch31 == -1:
    spisok_close = spisok_practicy
  else:
    spisok_close = [spisok_practicy[ch31]]

  for el in spisok_close:
      payload = payload_rows_practicy(
                                      dates,el["group_id"],
                                      el["subject_id"],
                                      0 if (el['id']+1)%3==0 else el["sub_group_id"]
                                    )

      response = requests.post(url_tab_rows, headers=headers, data=payload)

      data = response.json()
      print(data['rows'][0]['student_name'],el['group'])

      rows = data['rows'][0]['lessons']
      # print(rows)
      # return 0
      with open(diir+"\\практика\\rasp_"+el['group']+'.txt', encoding="utf-8") as file:
      # считываем строчки из файла
        try:
          lines = file.readlines()
          for i in range(len(lines)):
              name_lessons = lines[i]
              # print(name)
              les_id = rows[i]['id']
              # print(les_id,name)
              payload_save = payload_rows_practicy_save_tema(
                              les_id,el['student_id'],
                              dates,el['group_id'],
                              el['subject_id'],
                              0 if (el['id']+1)%3==0 else el["sub_group_id"],
                              name_lessons
                            )
              
              # print(payload_save)
              response = requests.post(url_save, headers=headers, data=payload_save)
              data = response.json()
              print(el['group'])
              print(i, response.status_code, data)

            
        except Exception as e:
            print(1,e)

        finally:
            file.close()
            print()
        # input()

def saveThemesTeory(diir,ch31):

  if ch31 == -1:
    spisok_close = spisok
  else:
    spisok_close = [spisok[ch31]]

  for name in spisok_close:
    payload_tab_rows = {
      "unit_id": 22,
      "period_id":	30,
      "date_from":	"2022-09-01T00:00:00",
      "date_to":	dates,
      "practical":	"",
      "slave_mode":	"",
      "month":	"",
      "group_id":	name['group_id'],
      "subject":	"0",
      "subject_gen_pr_id":	"0",
      "exam_subject_id":	"0",
      "subject_sub_group_obj":	"{\"subject_id\": "+name['subject_id']+"}",
      "subject_id":	name['subject_id'],
      "view_lessons":	"false"
  }
    response = requests.post(url_tab_rows, headers=headers, data=payload_tab_rows)
    # подучаем все столбцы
    # так как выдаёт всех студентов со всеми столбцами(попахивает бредом)
    # поэтому мы берём 0 элемент
    data = response.json()
    rows = data['rows'][0]['lessons']
    
    with open(diir+"\\лекции\\rasp_"+name['group']+'.txt', encoding="utf-8") as file:
      # считываем строчки из файла
      try:
        lines = file.readlines()
        for i in range(len(lines)):
            name_lessons = lines[i]
            # print(name)
            les_id = rows[i]['id']
            # print(les_id,name)
            payload_save = {
                "lesson_id": les_id,
                "student_id": name['student_id'],
                "unit_id": "22",
                "period_id": "30",
                "date_from": "2022-09-01T00:00:00",
                "date_to": dates,
                "practical": "",
                "slave_mode": "1",
                "month": "",
                "group_id": name['group_id'],
                "subject": "0",
                "subject_gen_pr_id": "0",
                "exam_subject_id": "0",
                "subject_sub_group_obj":	"{\"subject_id\": "+name['subject_id']+"}",
                "subject_id": name['subject_id'],
                "view_lessons": "false",
                "lesson_subject": name_lessons
            }

            response = requests.post(url_save, headers=headers, data=payload_save)
            data = response.json()
            print(name['group'])
            print(i, response.status_code, data)

            # print(lines[i], rows[i]['id'])
        #   text =i.rstrip()
        #   print(text)
      except Exception as e:
          print(e)

      finally:
          file.close()
          print()

def examinationRows(ch4:int):
  
  if ch4==1:
    for el in spisok:
      payload = payload_rows_teory(dates,el["group_id"],el["subject_id"])
      response = requests.post(url_tab_rows, headers=headers, data=payload)

      data = response.json()
      print(data['rows'][0]['student_name'],el['group'])

      rows = data['rows'][0]['lessons']
      for i in rows:
        print(i['id'],i['date'])
      # input()
  else:
    for el in spisok_practicy:
      payload = payload_rows_practicy(
                                      dates,
                                      el["group_id"],
                                      el["subject_id"],
                                      0 if (el['id']+1)%3==0 else el["sub_group_id"]
                                    )

      response = requests.post(url_tab_rows, headers=headers, data=payload)

      data = response.json()
      print(data['rows'][0]['student_name'],el['group'])

      rows = data['rows'][0]['lessons']
      for i in rows:
        print(i['id'],i['date'])
      # input()


def closeTheory(diir,ch51:int):
  spisok_close = ""
  if ch51 == -1:
    spisok_close = spisok
  else:
    spisok_close = [spisok[ch51]]
  
  for el in spisok_close:
    payload = payload_rows_teory(dates,el["group_id"],el["subject_id"])
    response = requests.post(url_tab_rows, headers=headers, data=payload)
    data = response.json()
    rows = data['rows'][0]['lessons']

    with open(diir+"\\лекции\\rasp_"+el['group']+'.txt', encoding="utf-8") as file:
    # считываем строчки из файла
      try:
        lines = file.readlines()
        for i in range(len(lines)):
            # name_lessons = lines[i]
            # print(name)
            les_id = rows[i]['id']
            # print(les_id,name)
            payload_save = {
                "lesson_id": les_id,
                "student_id": el['student_id'],
                "unit_id": "22",
                "period_id": "30",
                "date_from": "2022-09-01T00:00:00",
                "date_to": dates,
                "practical": "",
                "slave_mode": "1",
                "month": "",
                "group_id": el['group_id'],
                "subject": "0",
                "subject_gen_pr_id": "0",
                "exam_subject_id": "0",
                "subject_sub_group_obj":	"{\"subject_id\": "+el['subject_id']+"}",
                "subject_id": el['subject_id'],
                # "view_lessons": "false",
                # "lesson_subject": name_lessons
            }

            response = requests.post(url_close, headers=headers, data=payload_save)
            data = response.json()
            print(el['group'])
            print(i, response.status_code, data)

            # print(lines[i], rows[i]['id'])
        #   text =i.rstrip()
        #   print(text)
      except Exception as e:
          print(e)

      finally:
          file.close()
          print()


def closePractic(diir, ch51: int):
  spisok_close = ""
  if ch51 == -1:
    spisok_close = spisok_practicy
  else:
    spisok_close = [spisok_practicy[ch51]]

  for el in spisok_close:
    payload = payload_rows_practicy(
      dates, el["group_id"],
      el["subject_id"],
      0 if (el['id']+1) % 3 == 0 else el["sub_group_id"]
    )
    response = requests.post(url_tab_rows, headers=headers, data=payload)

    data = response.json()
    rows = data['rows'][0]['lessons']

    with open(diir+"\\практика\\rasp_"+el['group']+'.txt', encoding="utf-8") as file:
      # считываем строчки из файла
      try:
          lines = file.readlines()
          for i in range(len(lines)):
            # name_lessons = lines[i]
            # print(name)
            les_id = rows[i]['id']
            # print(les_id,name)
            payload_save = {
              "lesson_id": les_id,
              "student_id": el['student_id'],
              "practical": "1",
              "unit_id": "22",
              "period_id": "30",
              "date_from": "2022-09-01T00:00:00",
              "date_to": dates,
              "slave_mode": "1",
              "month": "",
              "group_id": el['group_id'],
              "subject": "0",
              "subject_gen_pr_id": "0",
              "exam_subject_id": "0",
              "subject_sub_group_obj": "",
              "subject_id": el['subject_id'],
              "view_lessons": "false",
              "subperiod": "399",
              "mark": ""
            }
            if (el['id']+1) % 3 == 0:
              payload["subject_sub_group_obj"] = "{\"subject_id\": "+el['subject_id']+"}"
            else:
              payload["subject_sub_group_obj"] = "{\"subject_id\": " + \
                el['subject_id']+", \"sub_group_id\": "+el['subject_id']+"}"

            response = requests.post(
                url_close, headers=headers, data=payload_save)
            data = response.json()
            print(el['group'])
            print(i, response.status_code, data)

              # print(lines[i], rows[i]['id'])
          #   text =i.rstrip()
          #   print(text)
      except Exception as e:
        print(e)

      finally:
        file.close()
      print()


def openTheory(diir, ch61: int):
  spisok_close = ""
  if ch61 == -1:
    spisok_close = spisok
  else:
    spisok_close = [spisok[ch61]]
  
  for el in spisok_close:
    payload = payload_rows_teory(dates,el["group_id"],el["subject_id"])
    response = requests.post(url_tab_rows, headers=headers, data=payload)
    data = response.json()
    rows = data['rows'][0]['lessons']

    with open(diir+"\\лекции\\rasp_"+el['group']+'.txt', encoding="utf-8") as file:
    # считываем строчки из файла
      try:
        lines = file.readlines()
        for i in range(len(lines)):
            # name_lessons = lines[i]
            # print(name)
            les_id = rows[i]['id']
            # print(les_id,name)
            payload_save = {
                "lesson_id": les_id,
                "student_id": el['student_id'],
                "unit_id": "22",
                "period_id": "30",
                "date_from": "2022-09-01T00:00:00",
                "date_to": dates,
                "practical": "",
                "slave_mode": "1",
                "month": "",
                "group_id": el['group_id'],
                "subject": "0",
                "subject_gen_pr_id": "0",
                "exam_subject_id": "0",
                "subject_sub_group_obj":	"{\"subject_id\": "+el['subject_id']+"}",
                "subject_id": el['subject_id'],
            }

            response = requests.post(url_open, headers=headers, data=payload_save)
            data = response.json()
            print(el['group'])
            print(i, response.status_code, data)

            # print(lines[i], rows[i]['id'])
        #   text =i.rstrip()
        #   print(text)
      except Exception as e:
          print(e)

      finally:
          file.close()
          print()


def openPractic(diir, ch61: int):
  spisok_close = ""
  if ch61 == -1:
    spisok_close = spisok_practicy
  else:
    spisok_close = [spisok_practicy[ch61]]        

  for el in spisok_close:
    payload = payload_rows_practicy(
      dates, el["group_id"],
      el["subject_id"],
      0 if (el['id']+1) % 3 == 0 else el["sub_group_id"]
    )
    response = requests.post(url_tab_rows, headers=headers, data=payload)

    data = response.json()
    rows = data['rows'][0]['lessons']

    with open(diir+"\\практика\\rasp_"+el['group']+'.txt', encoding="utf-8") as file:
      # считываем строчки из файла
      try:
          lines = file.readlines()
          for i in range(len(lines)):
            # name_lessons = lines[i]
            # print(name)
            les_id = rows[i]['id']
            # print(les_id,name)
            payload_save = {
              "lesson_id": les_id,
              "student_id": el['student_id'],
              "practical": "1",
              "unit_id": "22",
              "period_id": "30",
              "date_from": "2022-09-01T00:00:00",
              "date_to": dates,
              "slave_mode": "1",
              "month": "",
              "group_id": el['group_id'],
              "subject": "0",
              "subject_gen_pr_id": "0",
              "exam_subject_id": "0",
              "subject_sub_group_obj": "",
              "subject_id": el['subject_id'],
              "view_lessons": "false",
              "subperiod": "399",
              "mark": ""
            }
            if (el['id']+1) % 3 == 0:
              payload["subject_sub_group_obj"] = "{\"subject_id\": "+el['subject_id']+"}"
            else:
              payload["subject_sub_group_obj"] = "{\"subject_id\": " + \
                el['subject_id']+", \"sub_group_id\": "+el['subject_id']+"}"

            response = requests.post(
                url_open, headers=headers, data=payload_save)
            data = response.json()
            print(el['group'])
            print(i, response.status_code, data)

              # print(lines[i], rows[i]['id'])
          #   text =i.rstrip()
          #   print(text)
      except Exception as e:
        print(e)

      finally:
        file.close()
      print()