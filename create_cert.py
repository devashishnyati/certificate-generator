

from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageFilter
import numpy as np
import pandas as pd
import textwrap
import math
import dlib
import cv2
from datetime import datetime



def dist(x0, y0, x1, y1):
    a = (x1 - x0)**2 + (y1 - y0)**2
    b = math.sqrt(a)
    return b


def add_text(draw_text, text, box_size, font, color):
    box_size = [ int(x) for x in box_size ]
    text_x2, text_y2,  text_x1, text_y1 = box_size 
    
    text_w, text_h = draw_text.textsize(text, font=font)

    text_y = text_y2 + (text_y1 - text_y2 - text_h)//2
    
    MAX_W, MAX_H = text_x1- text_x2, text_y1 - text_y2
    
    current_h, pad = text_y, 5
    
    para = textwrap.wrap(text, width=55)
    
    for line in para:
        text_w, text_h = draw_text.textsize(line, font=font)
        text_x = text_x2 + (text_x1 - text_x2 - text_w)//2
        draw_text.text((text_x, current_h), line, color, align='center', font=font)
        current_h += text_h + pad

def read_data(filename):
    df = pd.read_csv(filename)
    return df

def create_cert(j, cert_temp, name_box, rec_box, date_box, photo_start_coordinates, text_size):


    name_font_size, rec_font_size, date_font_size = text_size
    image_name = j['EMPLOYEE NAME']
    pil_image = Image.open('photos/' + image_name + '.jpeg')
    
    name_text = j['EMPLOYEE NAME']
    rec_text = 'Performer of the year 2019-20 ' + j['CATEGORY'] + ' ' + j['Product'] + ' as ' + j['DESIGNATION'] + ' under category of ' + j['TROPHY TYPE']
    date_text = datetime.strptime(str(datetime.today().strftime('%m/%d/%Y')), '%m/%d/%Y')
    date_text = date_text.strftime('%b %d, %Y')
    
    rec_font = ImageFont.truetype("fonts/rec-font.ttf", size=rec_font_size)
    name_font = ImageFont.truetype("fonts/name-font.ttf", size=name_font_size)
    date_font = ImageFont.truetype("fonts/date-font.ttf", size=date_font_size)
    
    newsize = (200, 200) 
    
    img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    height, width, channels = img.shape


    gray = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)

    faces = detector(gray)

    mask = Image.new('L', (width, height))
    mask_draw = ImageDraw.Draw(mask)
    for face in faces:
        landmarks = predictor(image=gray, box=face)

        x = landmarks.part(27).x
        y = landmarks.part(27).y
        radius  = int(min (dist(x, y, width, y), dist(x, y, x, 0), dist(x, y, x, height), dist(x, y, 0, y)))
        cv2.circle(img=img, center=(x, y), radius=radius, color=(0, 255, 0), thickness=1)

        mask_draw.ellipse((x - radius, y- radius, x + radius, y + radius), fill=255)
        pil_image.putalpha(mask)

        pil_image = pil_image.crop((x - radius, y- radius, x + radius, y + radius)) 
        mask = mask.crop((x - radius, y- radius, x + radius, y + radius)) 

        break

    back_im = cert_temp.copy()
    back_im.paste(pil_image.resize(newsize), photo_start_coordinates, mask.resize(newsize))
    draw_text = ImageDraw.Draw(back_im)



    add_text(draw_text, name_text, name_box, name_font, (0,0,0))
    add_text(draw_text, rec_text, rec_box, rec_font, (0,0,255))
    add_text(draw_text, date_text, date_box, date_font, (0,0,0))



    back_im.save('cert/' + image_name + '.pdf', quality=100)

if __name__ == "__main__":
    template_map = {
        '1' : {
            'file_name': 'md_template.jpg', 
            'name_box' : [1003,822,1351,871],
            'rec_box' : [698,919,1627,988],
            'date_box' : [807,1067,1084,1121],
            'photo_start_coordinates' : [1056,567]
            },
        '2' : {
            'file_name': 'director_template.jpg', 
            'name_box' : [1003,822,1351,871],
            'rec_box' : [698,919,1627,988],
            'date_box' : [862,1129,591,1084],
            'photo_start_coordinates' : [1056,567]
            },
        '3' : {
            'file_name': 'vp_template.jpg', 
            'name_box' : [1003,822,1351,871],
            'rec_box' : [698,919,1627,988],
            'date_box' : [862,1129,591,1084],
            'photo_start_coordinates' : [1056,567]
            }
        }
    text_size = [35, 30, 25]
    
        
    file_name = input('Enter the file name with path: ')
    df = read_data(file_name)
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("utils/shape_predictor_68_face_landmarks.dat")

    template_type = ''
    while template_type not in ('1','2','3'):
        template_type = input('Enter the certificate type (number 1,2 or 3...):\n1. MD Certificate\n2. Director Certificate\n3. VP Certificate\n')

    cert_temp_name = template_map[template_type]['file_name']
    change_position_bool = input('Do you want to change the name, recognition, date box and photo position? Y or N? ')
    if change_position_bool == 'Y' or change_position_bool ==' y' :
        name_box = input('Enter the name box position. \nThe current positions are: ' + str(template_map[template_type]['name_box']) + '\n')
        name_box = name_box.split(',')
        rec_box = input('Enter the rec box position. \nThe current positions are: ' + str(template_map[template_type]['rec_box']) + '\n') 
        rec_box = rec_box.split(',')
        date_box = input('Enter the date box position. \nThe current positions are: ' + str(template_map[template_type]['date_box']) + '\n') 
        date_box = date_box.split(',')
        photo_start_coordinates = input('Enter the photo start coordinates. \nThe current positions are: ' + str(template_map[template_type]['photo_start_coordinates']) + '\n') 
        photo_start_coordinates = photo_start_coordinates.split(',')
        photo_start_coordinates = [int(x) for x in photo_start_coordinates]
    else:
        name_box, rec_box, date_box, photo_start_coordinates = template_map[template_type]['name_box'], template_map[template_type]['rec_box'], template_map[template_type]['date_box'], template_map[template_type]['photo_start_coordinates']
    
    change_text_size_bool = input('Do you want to change the name, recognition and date text size? Y or N? ')
    if change_text_size_bool == 'Y' or change_text_size_bool ==' y' :
        text_size = input('Enter the name, recognition and date text size. \nThe current sizes are: ' + str(text_size) + '\n')
        text_size = text_size.split(',')
        text_size = [int(x) for x in text_size]
    
    cert_temp = Image.open("templates/" + cert_temp_name)
    print('Creating Certificates.....')
    for i, j in df.iterrows():
        create_cert(j, cert_temp, name_box, rec_box, date_box, photo_start_coordinates, text_size)