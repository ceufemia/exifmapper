import exifread
import re


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
        second = str(int(second_num) / int(second_den))
    else:
        second = second_num
    return[degree, minute, second]


def extract_exif(imgfile):
    image = open(imgfile, 'rb')

    tags = exifread.process_file(image)

    for tag in tags:
        if tag == 'GPS GPSLatitude':
            lat = str(tags[tag])
            lat_coor = gen_coordinate_array(lat)
        elif tag == 'GPS GPSLatitudeRef':
            latref = str(tags[tag])
        elif tag == 'GPS GPSLongitudeRef':
            longref = str(tags[tag])
        elif tag == 'GPS GPSLongitude':
            lon = str(tags[tag])
            long_coor = gen_coordinate_array(lon)
        elif tag == 'Image DateTime':
            dt = str(tags[tag])

    print lat_coor[0] + ' ' + lat_coor[1] + '\' ' + lat_coor[2] + '\"' + str(latref) + ', ' + long_coor[0] + ' ' + \
          long_coor[1] + '\'' + long_coor[2] + '\"' + str(longref) + ' at ' + dt


extract_exif('C:\Users\T530\Downloads\IMG_20180527_232015.jpg')
