
import time
import os

from PIL import Image
from celery import Celery

app = Celery(
    'taskqueue', # 이건 파일 이름과 같아야 한다.
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
)

@app.task
def make_thumbnail(path, width, height):
    filepath, ext = os.path.splitext(path) # 파일의 경로와 파일의 확장자를 분류한다. ('jake', '.jpg')
    output_path = '{}_thumb{}'.format(filepath, ext)

    if os.path.exists(output_path):
        return output_path

    im = Image.open(path)
    im.thumbnail((width, height, ), Image.ANTIALIAS) # ANTIALIAS는 튀는 부분을 막아준다..(검색해봐야지)
    im.save(output_path)
    im.close()

    return output_path

@app.task
def add(a, b):
    time.sleep(5)
    return a+b

@app.task
def sum2(values):
    time.sleep(5)
    return sum(values)
