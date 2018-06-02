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
    dt = " "

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


def mark_map(lat, lon, dt):
    import folium
    from folium.plugins import MarkerCluster
    map_osm = folium.Map(location=[40.752759, -73.977251], zoom_start=10)

    stations = folium.FeatureGroup(name='Pictures')
    stations.add_child(folium.Marker([lat, lon], popup=dt))
    map_osm.add_child(stations)
    map_osm.save('map.html')


exif_data = extract_exif('pic1.jpg')
mark_map(float(exif_data[0]), float(exif_data[1]), exif_data[2])
