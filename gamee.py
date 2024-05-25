import requests
import urllib.parse
import json
import time
import subprocess
# URL dan headers
url = "https://api.service.gameeapp.com/"
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'origin': 'https://cf.seeddao.org',
    'priority': 'u=1, i',
    'referer': 'https://cf.seeddao.org/',
}

# Fungsi untuk membaca initData dari file
def read_initdata_from_file(filename):
    initdata_list = []
    with open(filename, 'r') as file:
        for line in file:
            initdata_list.append(line.strip())
    return initdata_list


def get_nama_from_init_data(init_data):
    parsed_data = urllib.parse.parse_qs(init_data)
    if 'user' in parsed_data:
        user_data = parsed_data['user'][0]
        data = ""
        user_data_json = urllib.parse.unquote(user_data)
        user_data_dict = json.loads(user_data_json)
        if 'first_name' in user_data_dict:
            data = user_data_dict['first_name']
        if 'last_name' in user_data_dict:
            data = data + " " + user_data_dict['last_name']
        if 'username' in user_data_dict:
            data = data + " " + f"({user_data_dict['username']})"
        return data
    return None

# Fungsi untuk melakukan start session
def start_session():
    response = requests.post('https://seeddao.org/api/v1/seed/claim',{}, headers=headers)
    return response


def claim_harian():
    response = requests.post('https://seeddao.org/api/v1/login-bonuses',{},headers=headers)
    return response

# Fungsi untuk menjalankan operasi untuk setiap initData
def process_initdata(init_data):
    # Login
    nama = get_nama_from_init_data(init_data)
    print(nama)
    headers['telegram-data'] = init_data
    start_response = start_session()
    daily_response = claim_harian()
    if start_response.status_code == 200:
        start_data = start_response.json()
        print("Mine Started")
    else :
        print('Belum Waktunya Claim')

    if daily_response.status_code == 200:
        daily_data = daily_response.json
        print("Ambil Daily")
    else :
        print('Sudah Ambil Daily')
    
                

# Main program
def main():
    initdata_file = "initdata.txt"
    
    while True:
        initdata_list = read_initdata_from_file(initdata_file)
        
        for init_data in initdata_list:
            process_initdata(init_data.strip())
            print("\n")
        
        # Delay sebelum membaca ulang file initData
        time.sleep(0)  # Delay 60 detik sebelum membaca kembali file initData

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        subprocess.run(["python3.10", "gamee.py"])
