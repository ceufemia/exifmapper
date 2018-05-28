import exifread
import re

image = open('C:\Users\T530\Downloads\IMG_20180527_232015.jpg', 'rb')

tags = exifread.process_file(image)


def gen_coordinate_array(coor):
    degree_regex = re.compile(r'(\[)(\d{1,3})(,)')
    minute_regex = re.compile(r'(, )(\d{1,3})(,)')
    second_num_regex = re.compile(r'(, )(\d+)([/\]])')
    second_den_regex = re.compile(r'(/)(\d+)(\])')
    degree = degree_regex.search(coor).group(2)
    minute = minute_regex.search(coor).group(2)
    second_num = second_num_regex.search(coor).group(2)
    second_den = second_den_regex.search(coor).group(2)
    if second_den:
        second = second_num / second_den
    else:
        second = second_num
    return[degree, minute, second]


for tag in tags:
    if tag =='GPS GPSLatitude':
        lat = str(tags[tag])
        gen_coordinate_array(lat)
        print lat_degree + ', ' + lat_minute + ', ' + lat_second
        '''lat_degree = degree_regex.search(lat).group(2)
        lat_minute = minute_regex.search(lat).group(2)
        second_num = second_den_regex.search(lat).group(2)
        second_den = second_den_regex.search(lat).group(2)
        if second_den:
            lat_second = second_num/second_den
        else:
            lat_second = second_num'''

    elif tag == 'GPS GPSLatitudeRef':
        latref = tags[tag]
        print latref
    elif tag=='GPS GPSLongitudeRef':
        longref = tags[tag]
        print longref
    elif tag == 'GPS GPSLongitude':
        long = tags[tag]
        print long
    elif tag == 'Image DateTime':
        dt = tags[tag]
        print dt

