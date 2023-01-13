import re 
import requests
import os
from dotenv import load_dotenv
load_dotenv()

import spisok_student as s


dates_from = os.getenv('DATES_FROM')
dates = os.getenv('DATES')
cookie = os.getenv('COOKIE')
diir = os.getenv('DIIR')

url_tab_rows = "https://ssuz.vip.edu35.ru/actions/register/lessons_tab/lessons_tab_rows"
url_save = "https://ssuz.vip.edu35.ru/actions/register/lessons_tab/lessons_tab_save_work_lesson_subject"
url_close = "https://ssuz.vip.edu35.ru/actions/register/lessons_tab/lessons_tab_close_lesson_action"
url_open = "https://ssuz.vip.edu35.ru/actions/register/lessons_tab/lessons_tab_open_lesson_action"
name = ''
les_id = 0

spisok = s.spisok
spisok_practicy = s.spisok_practicy

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
    "date_from":dates_from,
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
    "date_from":dates_from,
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
              "date_from":dates_from,
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

def createFile(ch1):
  diirloc = diir
  spisok0 = ''

  if(ch1==0):
    diirloc = diirloc+'\\лекции'
    spisok0 = spisok
  elif(ch1==1):
    diirloc = diirloc+'\\практика'
    spisok0 = spisok_practicy


  for name in spisok0:
    try:
      with open(diirloc+"\\"+name['group']+'.txt','w',encoding="utf-8") as file2:
        print(name['group'])
    except Exception as e:
      print(e)
    finally:
      file2.close()

def dubleFileAll(ch2,ch21):
  diirloc = diir

  if ch2==1:
    diirloc = diirloc+'\\лекции'
    spisok1 = [spisok[ch21]]

  elif ch2==2:
    diirloc = diirloc+'\\практика'
    spisok1 = [spisok_practicy[ch21]]

  else:
    print('Такого действия нет')
  spisok1 = spisok

  for name in spisok1:
    data_list= []
    with open(diirloc+"\\"+name['group']+'.txt',encoding="utf-8") as file:
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
      with open(diirloc+"\\rasp_"+name['group']+'.txt','w',encoding="utf-8") as file2:
        # file2.write("\n".join(spisok).join("\n"));
        for item in data_list:
          file2.write("%s\n" % item)
          

    except Exception as e:
      print(e)

    finally:
      # print(name['group'],'Готово')
      file2.close()

def saveThemesPracticy(ch31):
  diirloc = diir

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
      with open(diirloc+"\\практика\\rasp_"+el['group']+'.txt', encoding="utf-8") as file:
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

def saveThemesTeory(ch31):
  diirloc = diir

  if ch31 == -1:
    spisok_close = spisok
  else:
    spisok_close = [spisok[ch31]]

  for name in spisok_close:
    payload_tab_rows = {
      "unit_id": 22,
      "period_id":	30,
      "date_from":dates_from,
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
    
    with open(diirloc+"\\лекции\\rasp_"+name['group']+'.txt', encoding="utf-8") as file:
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
                "date_from":dates_from,
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


def closeTheory(ch51:int):
  diirloc = diir

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

    with open(diirloc+"\\лекции\\rasp_"+el['group']+'.txt', encoding="utf-8") as file:
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
                "date_from": dates_from,
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


def closePractic( ch51: int):
  diirloc = diir

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

    with open(diirloc+"\\практика\\rasp_"+el['group']+'.txt', encoding="utf-8") as file:
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
              "date_from":dates_from,
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


def openTheory( ch61: int):
  diirloc = diir
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

    with open(diirloc+"\\лекции\\rasp_"+el['group']+'.txt', encoding="utf-8") as file:
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
                "date_from":dates_from,
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


def openPractic( ch61: int):
  diirloc = diir
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

    with open(diirloc+"\\практика\\rasp_"+el['group']+'.txt', encoding="utf-8") as file:
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
              "date_from":dates_from,
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