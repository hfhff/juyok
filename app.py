from flask import Flask,render_template, request
import os
import openai
from play import main

app = Flask(__name__)

with open("chatgpt.env") as env:
         for line in env:
            key, value = line.strip().split("=")
            os.environ[key] = value

openai.api_key = os.environ.get("API_KEY")

@app.route('/')
def index():
     return render_template('page.html')

@app.route('/result', methods=['GET','POST'])
def result():
    user_num1 = str(request.form.get("value1"))
    user_num2 = str(request.form.get("value2"))
    user_num3 = str(request.form.get("value3"))
    user_num4 = str(request.form.get("value4"))
    user_num5 = str(request.form.get("value5"))
    user_num6 = str(request.form.get("value6"))

    byte = user_num1 + user_num2 + user_num3 + user_num4 + user_num5 + user_num6
    choice, byte2, choice2 = main(byte)
    if request.method == "POST":
            if "user_input" in request.form:
                prompt = request.form["user_input"]
            else:
                prompt = None

            if prompt is not None:  # prompt 값이 존재하면 처리
                conversation = [
                      {
                    "role": "system",
                    "content": f"당신은 정약용의 <주역사전> 전문가입니다. {choice}가 <주역사전>에서 어떤 의미를 가지는 지 설명하고,{choice}에 맞추어 사용자가 쓴 고민에 대한 답을 해줍니다."
                },
                {
                    "role": "user",
                    "content": prompt
                }
                ]
                # openai.FineTune.create(
                # model="text-davinci-003",
                # # examples=[
                #     {
                #         "text": "",
                #         "label": ""
                #     },
                    
                # ],
                # epochs=5
            # )
                response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation,
                temperature=0.7,
                max_tokens=1000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
                )
                ai_response = response['choices'][0]['message']['content']
                conversation.append({"role": "assistant", "content": ai_response })
    return render_template('result.html', conversation=conversation, choice=choice, byte = byte, byte2 = byte2, choice2 = choice2)

if __name__ == '__main__':
    app.run(debug=True)