import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta



user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

    # Set up headers with the User-Agent
headers = {
        "User-Agent": user_agent,
        # You can add other headers here if needed
    }

def login(username, password):
    login_url = "https://fridasv.com/login"
    session = requests.Session()
    response = session.get(login_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    csrf_token_login = soup.find("input", {"name": "_token"})
    csrf_token_login_value = csrf_token_login.get("value")

    login_data = {
        "_token": csrf_token_login_value,
        "username": username,
        "password": password,
    }

    response_login = session.post(login_url, headers=headers, data=login_data)

    if response_login.status_code == 200:
        print("Login Success")
        return response_login.cookies.get_dict()
    else:
        print(f"Login Failed with status code: {response_login.status_code}")
        print("Response Content:", response_login.text)
        print("Response Headers:", response_login.headers)
        return None



def submitForm(username, password):
    cookies = login(username, password)
    url = "https://fridasv.com/mahasiswa/form-daily/jurnal-harian"
    
    session = requests.Session()
    response_csrf = session.get(url,headers=headers,cookies=cookies)
    soup = BeautifulSoup(response_csrf.text, "html.parser")

    csrf_token_form = soup.find("input", {"name": "_token"})
    csrf_token_form_value = csrf_token_form.get("value")
    print("ini token nya"+csrf_token_form_value)
    
    headers_form = {
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "id,en-US;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "multipart/form-data; boundary=---------------------------29895619081262927391393009917",
    "Origin": "https://fridasv.com",
    "Referer": "https://fridasv.com/mahasiswa/form-daily/jurnal-harian",
    }
    # Define the form data template
    # Define the form data template
    form_data_template = """-----------------------------29895619081262927391393009917
Content-Disposition: form-data; name="_token"

{csrf_token_form_value}
-----------------------------29895619081262927391393009917
Content-Disposition: form-data; name="tanggal"

{date}
-----------------------------29895619081262927391393009917
Content-Disposition: form-data; name="waktu_mulai"

08:00
-----------------------------29895619081262927391393009917
Content-Disposition: form-data; name="waktu_selesai"

16:00
-----------------------------29895619081262927391393009917
Content-Disposition: form-data; name="kegiatan"

{kegiatan}
-----------------------------29895619081262927391393009917--
"""
     # Set the start and end dates
    start_date = datetime(2023, 10, 1)
    end_date = datetime(2023, 10, 3)

    # Array of activities
    kegiatan_array = [
        "belajar layout responsif dengan flexbox1",
        "mengerjakan tugas2",
        "diskusi dengan teman2",
        # Add more activities as needed
    ]
    # Iterate over the dates
    current_date = start_date
    url_form = "https://fridasv.com/mahasiswa/form-daily/jurnal-harian/submit"
    while current_date <= end_date:
        # Check if the current day is Monday to Friday
        if 0 <= current_date.weekday() <= 4:
            # Format the date
            formatted_date = current_date.strftime("%m/%d/%Y")

            # Select an activity from the array (cycling through activities)
            kegiatan = kegiatan_array[current_date.day % len(kegiatan_array)]

            # Replace the placeholders in the form data template
            form_data = form_data_template.format(date=formatted_date, kegiatan=kegiatan, csrf_token_form_value=csrf_token_form_value)

            # Send the HTTP request
            response = session.post(url_form, headers=headers_form, data=form_data)

            # Print the result
            print(f"Date: {formatted_date}, Kegiatan: {kegiatan}, Status Code: {response.status_code}")

        # Move to the next day
        current_date += timedelta(days=1)


username = "example"
password = "example"
submitForm(username, password)