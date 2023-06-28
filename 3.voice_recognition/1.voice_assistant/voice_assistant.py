import speech_recognition as sr
from datetime import datetime
from io import BytesIO
from navertts import NaverTTS
from pydub import AudioSegment
from pydub.playback import play
import gtts

r = sr.Recognizer()

microphone = sr.Microphone()


def rule_based_answer(ai_answer):
    print(ai_answer)
    tts = NaverTTS(ai_answer, lang="ko")
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp = BytesIO(fp.getvalue())
    my_sound = AudioSegment.from_file(fp, format="mp3")
    play(my_sound)


while True:
    with microphone as source:
        r.adjust_for_ambient_noise(source)
        print("음성 명령을 기다리는 중입니다.")
        audio = r.listen(source)

    try:
        user_command = r.recognize_google(audio, language="ko")

    except sr.UnknownValueError:
        print("인식할 수 없습니다.")

    except sr.RequestError as e:
        print("인식에 문제가 있습니다.", e)

    else:  # 음성이 잘 인식되었을 경우 실행
        print("인식 결과:", user_command)

        # 명령 분석 및 대답할 문자열
        if user_command == "종료":
            ai_answer = "종료합니다."
        elif "시간" in user_command:
            current_time = datetime.now()
            ai_answer = f"지금은 {current_time.hour}시 {current_time.minute}분 입니다."
        elif "날짜" in user_command:
            today = datetime.today()
            ai_answer = f"오늘은 {today.year}년 {today.month}월 {today.day}일 입니다."
        else:
            ai_answer = "알 수 없는 명령입니다."

        # 음성 합성 및 재생
        rule_based_answer(ai_answer)

        if user_command == "종료":
            break
