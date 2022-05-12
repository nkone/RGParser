from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter, Retry
import time
import datetime
import csv
import os
import sys

rg_5268ac = {
        "home_url": "http://192.168.1.254/xslt?PAGE=A_0_0",
        "wifi_url": "http://192.168.1.254/xslt?PAGE=C_2_1",
        "login_url":"http://192.168.1.254/xslt?PAGE=login_post",
        "access_code": "",
        }
bgw_210 = {
        'home_url': "http://192.168.1.254/cgi-bin/home.ha",
        'login_url': "http://192.168.1.254/cgi-bin/login.ha",
        'sys_url': "http://192.168.1.254/cgi-bin/sysinfo.ha",
        'voice_url': "http://192.168.1.254/cgi-bin/voice.ha",
        'lanstats_url': "http://192.168.1.254/cgi-bin/lanstatistics.ha",
        'Manufacturer': "",
        'Model_Number': "",
        'Serial_Number': "",
        'MAC_Address': "",
        '2.4ghz_SSID': "",
        '2.4ghz_Mode': "",
        '2.4ghz_Bandwidth': "",
        '2.4ghz_Current_Bandwidth': "",
        '2.4ghz_Current_Radio_Channel': "",
        #'2.4ghz_Radio_Channel_Selection': "",
        #'2.4ghz_Power_Level': "",
        'Guest_SSID': "",
        '5ghz_SSID': "",
        '5ghz_Mode': "",
        '5ghz_Bandwidth': "",
        '5ghz_Current_Bandwidth': "",
        '5ghz_Current_Radio_Channel': "",
        #'5ghz_Radio_Channel_Selection': "",
        #'5ghz_Power_Level': "",
        'First_Use_Date': "",
        'Time_Since_Reboot': "",
        'Software_Version': "",
        'Datapump_Version': "",
        'Hardware_Version': "",
        'Phone_Line_1': "",
        'Phone_Line_2': "",
        'Sync_Time': "",
        }
bgw_320 = {
        'home_url': "http://192.168.1.254/cgi-bin/home.ha",
        'login_url': "http://192.168.1.254/cgi-bin/login.ha",
        'sys_url': "http://192.168.1.254/cgi-bin/sysinfo.ha",
        'voice_url': "http://192.168.1.254/cgi-bin/voice.ha",
        'lanstats_url': "http://192.168.1.254/cgi-bin/lanstatistics.ha",
        'Manufacturer': "",
        'Model_Number': "",
        'Serial_Number': "",
        'MAC_Address': "",
        '2.4ghz_SSID': "",
        '2.4ghz_Mode': "",
        '2.4ghz_Bandwidth': "",
        '2.4ghz_Current_Bandwidth': "",
        '2.4ghz_Current_Radio_Channel': "",
        #'2.4ghz_Radio_Channel_Selection': "",
        #'2.4ghz_Power_Level': "",
        'Guest_SSID': "",
        '5ghz_SSID': "",
        '5ghz_Mode': "",
        '5ghz_Bandwidth': "",
        '5ghz_Current_Bandwidth': "",
        '5ghz_Current_Radio_Channel': "",
        #'5ghz_Radio_Channel_Selection': "",
        #'5ghz_Power_Level': "",
        'First_Use_Date': "",
        'Time_Since_Reboot': "",
        'Software_Version': "",
        'Hardware_Version': "",
        'Phone_Line_1': "",
        'Phone_Line_2': "",
        'Sync_Time': "",
        }
headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Content-Type': 'text/html',
        }

def parse_time(start, end, rg_model):
    m, s = divmod(int(end - start), 60)
    h, m = divmod(m, 60)
    
    rg_model['Sync_Time'] = str(h).zfill(2) + ':' + str(m).zfill(2) + ':' + str(s).zfill(2)
    print(f'Get time: {h:d}:{m:02d}:{s:02d}')

def dict_to_csv(rg_dict):
    desire_path = '/home/odroid/Desktop/Output'
    timestr = time.strftime("%Y-%m-%d_%H%M%S")
    csv_file = rg_dict['Serial_Number'] + "_" + timestr + ".csv"
    file_path = os.path.join(desire_path, csv_file)
    keys = rg_dict.keys()

    try:
        with open(file_path, 'w', newline='') as output_file:
            writer = csv.DictWriter(output_file, keys)
            writer.writeheader()
            writer.writerow(rg_dict)
    except IOError:
        print("I/O error")

def print_rg(rg_model):
    del rg_model['home_url']
    del rg_model['login_url']
    del rg_model['sys_url']
    del rg_model['voice_url']
    del rg_model['lanstats_url']
    #for value in rg_model:
    #    print(value, ':', rg_model[value])
    print("SSID: ", rg_model['2.4ghz_SSID'])
    print("Serial: ", rg_model['Serial_Number'])
    print("Time: ", rg_model['Sync_Time'])


def parse_bgw_210():
    start_time = time.time()
    retry = 1
    while True:
        try:
            #print("Try #: ", retry)
            response = requests.get(bgw_210['home_url'], headers=headers)
            if response.status_code == 200:
                break
        except:
            retry += 1
            if retry >= 30:
                print("Time limit exceeded")
                return
            time.sleep(5)
    end_time = time.time()
    parse_time(start_time, end_time, bgw_210)
    # Get SSID
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    label_container = soup.find_all(text='Network Name (SSID)')
    bgw_210['2.4ghz_SSID']=label_container[0].findNext('td').contents[0].text.strip()
    bgw_210['Guest_SSID']=label_container[1].findNext('td').contents[0].text.strip()
    bgw_210['5ghz_SSID']=label_container[2].findNext('td').contents[0].text.strip()

    # Get system info
    response = requests.get(bgw_210['sys_url'], headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    system_container = soup.find_all('tr')
    bgw_210['Manufacturer'] = system_container[0].find(text='Manufacturer').findNext('td').text
    bgw_210['Model_Number'] = system_container[1].find(text='Model Number').findNext('td').text
    bgw_210['Serial_Number'] = system_container[2].find(text='Serial Number').findNext('td').text
    bgw_210['Software_Version'] = system_container[3].find(text='Software Version').findNext('td').text
    bgw_210['MAC_Address'] = system_container[4].find(text='MAC Address').findNext('td').text
    bgw_210['First_Use_Date'] = system_container[5].find(text='First Use Date').findNext('td').text
    bgw_210['Time_Since_Reboot'] = system_container[6].find(text='Time Since Last Reboot').findNext('td').text
    bgw_210['Datapump_Version'] = system_container[8].find(text='Datapump Version').findNext('td').text
    bgw_210['Hardware_Version'] = system_container[9].find(text='Hardware Version').findNext('td').text

    # Get voice
    response = requests.get(bgw_210['voice_url'], headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    voice_container = soup.find_all('tr')
    phone_number = voice_container[1].findChildren('td')
    bgw_210['Phone_Line_1'] = phone_number[1].text
    bgw_210['Phone_Line_2'] = phone_number[2].text

    # Wait for 5ghz to boot up
    #time.sleep(120)

    # Get lan stats (wifi channel)
    response = requests.get(bgw_210['lanstats_url'], headers = headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    try:
        wifi_mode = soup.find("td", text="Mode").find_next_siblings('td')
        bgw_210['2.4ghz_Mode'] = wifi_mode[0].text
        bgw_210['5ghz_Mode'] = wifi_mode[1].text
    except:
        print("No wifi mode element")

    try:
        wifi_bandwidth = soup.find("td", text="Bandwidth").find_next_siblings('td')
        bgw_210['2.4ghz_Bandwidth'] = wifi_bandwidth[0].text
        bgw_210['5ghz_Bandwidth'] = wifi_bandwidth[1].text
    except:
        print("No bandwidth element")

    try:
        wifi_curr_bandwidth = soup.find("td", text="Current Bandwidth").find_next_siblings('td')
        bgw_210['2.4ghz_Current_Bandwidth'] = wifi_curr_bandwidth[0].text
        bgw_210['5ghz_Current_Bandwidth'] = wifi_curr_bandwidth[1].text
    except:
        print("No current bandwidth element")

    try:
        wifi_ch = soup.find("td", text="Current Radio Channel").find_next_siblings('td')
        bgw_210['2.4ghz_Current_Radio_Channel'] = wifi_ch[0].text
        bgw_210['5ghz_Current_Radio_Channel'] = wifi_ch[1].text
    except:
        print("No current radio element")
    print_rg(bgw_210)
    dict_to_csv(bgw_210)

def parse_bgw_320():
    start_time = time.time()
    retry = 1
    while True:
        try:
            #print("Try #: ", retry)
            response = requests.get(bgw_320['home_url'], headers=headers)
            if response.status_code == 200:
                break
        except:
            retry += 1
            if retry >= 30:
                print("Time limit exceeded")
                return
            time.sleep(5)
    end_time = time.time()
    parse_time(start_time, end_time, bgw_320)
    # Get SSID
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    label_container = soup.find_all(text='Network Name (SSID)')
    bgw_320['2.4ghz_SSID']=label_container[0].findNext('td').text.strip()
    bgw_320['Guest_SSID']=label_container[1].findNext('td').text.strip()
    bgw_320['5ghz_SSID']=label_container[2].findNext('td').text.strip()

    # Get system info
    response = requests.get(bgw_320['sys_url'], headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    system_container = soup.find_all('tr')
    bgw_320['Manufacturer'] = system_container[0].find(text='Manufacturer').findNext('td').text
    bgw_320['Model_Number'] = system_container[1].find(text='Model Number').findNext('td').text
    bgw_320['Serial_Number'] = system_container[2].find(text='Serial Number').findNext('td').text
    bgw_320['Software_Version'] = system_container[3].find(text='Software Version').findNext('td').text
    bgw_320['MAC_Address'] = system_container[4].find(text='MAC Address').findNext('td').text
    bgw_320['First_Use_Date'] = system_container[5].find(text='First Use Date').findNext('td').text
    bgw_320['Time_Since_Reboot'] = system_container[6].find(text='Time Since Last Reboot').findNext('td').text
    bgw_320['Hardware_Version'] = system_container[8].find(text='Hardware Version').findNext('td').text

    # Get voice
    response = requests.get(bgw_320['voice_url'], headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    voice_container = soup.find_all('tr')
    phone_number = voice_container[1].findChildren('td')
    bgw_320['Phone_Line_1'] = phone_number[1].text
    bgw_320['Phone_Line_2'] = phone_number[2].text

    # Wait for 5ghz to boot up
    time.sleep(120)

    # Get lan stats (wifi channel)
    response = requests.get(bgw_320['lanstats_url'], headers = headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    try:
        wifi_mode = soup.find("td", text="Mode").find_next_siblings('td')
        bgw_320['2.4ghz_Mode'] = wifi_mode[0].text
        bgw_320['5ghz_Mode'] = wifi_mode[1].text
    except:
        print("No wifi mode element")

    try:
        wifi_bandwidth = soup.find("td", text="Bandwidth").find_next_siblings('td')
        bgw_320['2.4ghz_Bandwidth'] = wifi_bandwidth[0].text
        bgw_320['5ghz_Bandwidth'] = wifi_bandwidth[1].text
    except:
        print("No bandwidth element")

    try:
        wifi_curr_bandwidth = soup.find("td", text="Current Bandwidth").find_next_siblings('td')
        bgw_320['2.4ghz_Current_Bandwidth'] = wifi_curr_bandwidth[0].text
        bgw_320['5ghz_Current_Bandwidth'] = wifi_curr_bandwidth[1].text
    except:
        print("No current bandwidth element")

    try:
        wifi_ch = soup.find("td", text="Current Radio Channel").find_next_siblings('td')
        bgw_320['2.4ghz_Current_Radio_Channel'] = wifi_ch[0].text
        bgw_320['5ghz_Current_Radio_Channel'] = wifi_ch[1].text
    except:
        print("No current radio element")
    #dict_to_csv(bgw_320)
    print_rg(bgw_320)

def usage():
    print("Usage: parser.py [Model]")
    print("Support model: bgw210, bgw320")

def main():
    if (len(sys.argv) != 2):
        usage()
        return
    if (sys.argv[1] == "bgw210"):
        parse_bgw_210()
    elif (sys.argv[1] == "bgw320"):
        parse_bgw_320()

if __name__ == "__main__":
    main()
