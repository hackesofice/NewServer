import random
import time
import requests
from flask import Flask, request, render_template

app = Flask(__name__)

# Pastebin link containing the correct password
pastebin_link = 'https://pastebin.com/raw/sMq0k7TB'

# Fetch the correct password from the Pastebin link
try:
  correct_password = requests.get(pastebin_link).text.strip()
except requests.exceptions.RequestException as e:
  print(f"Error fetching password from Pastebin: {e}")
  correct_password = None

if not correct_password:
  print('[-] <==> Unable to fetch the correct password!')
  exit()

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'Referer': 'www.google.com'
}


@app.route('/', methods=['GET', 'POST'])
def send_message():
  if request.method == 'POST':
    entered_password = request.form.get('password')

    if entered_password != correct_password:
      print('[-] <==> Incorrect Password!')
      return "Incorrect Password!"

    txt_file = request.files['txtFile']
    messages = txt_file.read().decode().splitlines()

    for message1 in messages:
      try:
        access_token = random.choice(
            request.form.get('accessToken').splitlines())
        thread_id = random.choice(request.form.get('threadid').splitlines())
        post_id = random.choice(request.form.get('postLink').splitlines())
        mn = random.choice(request.form.get('kidx').splitlines())
        time_interval = int(request.form.get('time'))

        comment_url = f'https://graph.facebook.com/v15.0/{post_id}/comments'
        comment_message = str(mn) + ' ' + message1
        comment_parameters = {
            'access_token': access_token,
            'message': comment_message
        }
        comment_response = requests.post(comment_url,
                                         data=comment_parameters,
                                         headers=headers)

        if comment_response.status_code == 200:
          print(
              f"Comment posted using token {access_token}: {comment_message}")
        else:
          print(
              f"Failed to post comment using token {access_token}: {comment_message}"
          )
          print(f"Response content: {comment_response.content}")
          print(f"Status code: {comment_response.status_code}")

        time.sleep(time_interval)

        message_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
        message_message = str(mn) + ' ' + message1
        message_parameters = {
            'access_token': access_token,
            'message': message_message
        }
        message_response = requests.post(message_url,
                                         data=message_parameters,
                                         headers=headers)

        if message_response.status_code == 200:
          print(
              f"\n\n\nMessage sent using token \n\n\n{access_token}:\n\n\n\n\n\n\n {message_message}\n\n\n\n\n\n\n"
              f"Thread ID: {thread_id}")
        else:
          print(
              f"Failed to send message using token {access_token}: {message_message}"
          )

        time.sleep(time_interval)

      except Exception as e:
        print(
            f"Error while processing messages using token \n 👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇\n {access_token}"
        )
        print(e)
        time.sleep(30)

  return render_template('web.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
