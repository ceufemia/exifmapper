import exifread
import re
import os
import folium
import webbrowser
from Tkinter import Tk
from tkFileDialog import askopenfilenames
from folium.plugins import MarkerCluster
from datetime import datetime


def get_pictures(directory):
    pictures = []
    for file1 in os.listdir(directory):
        if file1.endswith(".jpg"):
            pictures.append("Pics\\" + file1)
    return pictures


def get_coordinates(coor):
    degree_regex = re.compile(r'(\[)(\d{1,3})(,)')
    minute_regex = re.compile(r'(, )(\d{1,3})(,)')
    second_num_regex = re.compile(r'(, )(\d+)([/\]])')
    second_den_regex = re.compile(r'(/)(\d+)(\])')
    degree = degree_regex.search(coor).group(2)
    minute = minute_regex.search(coor).group(2)
    second_num = second_num_regex.search(coor).group(2)
    try:
        second_den = second_den_regex.search(coor).group(2)
        second = str(float(second_num) / float(second_den))
    except:
        second = second_num
    final_coor = float(degree) + float(minute)/60 + float(second)/(60*60)
    return final_coor


def extract_exif(imgfile):
    image = open(imgfile, 'rb')

    tags = exifread.process_file(image)
    lat_coor = 0
    latref = "N"
    long_coor = 0
    longref = "W"
    dt = "Unknown time"

    for tag in tags:
        if tag == 'GPS GPSLatitude':
            lat = str(tags[tag])
            lat_coor = get_coordinates(lat)
        elif tag == 'GPS GPSLatitudeRef':
            latref = str(tags[tag])
        elif tag == 'GPS GPSLongitudeRef':
            longref = str(tags[tag])
        elif tag == 'GPS GPSLongitude':
            lon = str(tags[tag])
            long_coor = get_coordinates(lon)
        elif tag == 'Image DateTime':
            dt = str(tags[tag])
    try:
        if longref == 'W':
            long_coor = long_coor*-1
    except:
        print "No Longitude Data provided"
    try:
        if latref == 'S':
            lat_coor = lat_coor*-1
    except:
        print "No Latitude Data provided"

    return [str(lat_coor), str(long_coor), imgfile + " taken at " + dt]


def mark_map(exifs):
    map_osm = folium.Map(location=[40.752759, -73.977251], zoom_start=10)
    stations = folium.FeatureGroup(name='Pictures')

    for exif in exifs:
        if exif[0] == 0 and exif[1] == 0 and dt == "Unknown time":
            pass
        else:
            stations.add_child(folium.Marker([float(exif[0]), float(exif[1])], popup=exif[2]))
            map_osm.add_child(stations)
    if not os.path.exists("Maps"):
        os.makedirs("Maps")

    return map_osm


Tk().withdraw()
pics = askopenfilenames()
exif_data = []
for picture in pics:
    exif_data.append(extract_exif(picture))
    picture_map = mark_map(exif_data)
savename = 'Maps\map' + datetime.today().strftime('%Y%m%d%H%M%S') + '.html'
picture_map.save(savename)
webbrowser.open('file://' + os.path.realpath(savename))
