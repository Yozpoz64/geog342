# import modules
import folium 
import webbrowser
import gpxpy
import matplotlib.pyplot as plt

# this is to change the working dir since spyder sucks at doing it
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

'''
PLACES
    -hurstmere road
    -vic park
    -st heliers
    -greenlane
    
get 300m segments from this area and plot as gpx https://www.gpsvisualizer.com/draw/

FACTORS
    -road quality
    -road surface type
    -cycle lane type
    -water/toilets/other facilities
    -bike parking
    -public transport connections
    -construction
'''

# constants
CENTRE = (-36.85, 174.75)
ZOOM = 12
TITLE = 'Cycling Index Map'
SUBTITLE = ('Shows cycling friendliness at chosen locations in Auckland. '
                'Created for GEOG342 Assignment 2.')
LINE_WEIGHT = 10
FACTORS = ['Road quality', 'Road surface type', 'Cycle lane type', 'Facilities', 
           'Bike parking', 'Public transport connection', 'Construction']


# function for getting folium map object
def get_map(centre=CENTRE, zoom=ZOOM, title=TITLE, subtitle=SUBTITLE):
    map_object = folium.Map(location=centre, zoom_start=zoom, 
                tiles='OpenStreetMap', 
                control_scale=True, height='85%')
    title = ('<h3 align="center" style="font-size:20px"><b>{}</b></h3>'
             '<h2 align="center" style="font-size:12px">{}</h2>'
                ).format(title, subtitle)
    map_object.get_root().html.add_child(folium.Element(title))
    return map_object


# get latitude/longitude pairs from gpx file
def get_coords(file):
    points = []
    this_file = open(file, 'r')
    gpx = gpxpy.parse(this_file)
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append(tuple([point.latitude, point.longitude]))
    return points


# calls other functions to build track and popup
def build_track(gpx_file, name, values, feature_group):
    track_points = get_coords(gpx_file)

    # set colour based on values
    if sum(values) <= 10:
        colour = 'red'
    elif sum(values) <= 25:
        colour = 'orange'
    elif sum(values) <= 35:
        colour = 'blue'
    else:
        colour = 'green'
    
    popup_html = ('<b>{}</b><br><br><b>{}:</b> {}<br><b>{}:</b> {}'
                  '<br><b>{}:</b> {}<br><b>{}:</b> {}<br><b>{}:</b> {}'
                  '<br><b>{}:</b> {}<br><b>{}:</b> {}<br>'
                   ).format(name, FACTORS[0], values[0], FACTORS[1], 
                            values[1], FACTORS[2], values[2], FACTORS[3],
                            values[3], FACTORS[4], values[4], FACTORS[5],
                            values[5], FACTORS[6], values[6])
    
    folium.PolyLine(track_points, weight=LINE_WEIGHT, color=colour,
                    tooltip=folium.Html(popup_html, script=True).render()
                    ).add_to(feature_group)
    
    
def map_photo(file, telemetry, feature_group):
    print(file)
    popup_html = '<img src={} width="250">'.format(file)
    folium.Marker(location=telemetry, icon=folium.Icon(icon='camera', prefix='fa'),
            tooltip=folium.Html(popup_html, script=True).render()).add_to(feature_group)
    
    
def plot_scores(values, location, axes):
    axes.bar(x=FACTORS, height=values)
    #axes.plot(FACTORS, values)
    plt.xticks(rotation=45)
    plt.title('Cycling Index Scores at {}'.format(location))
    axes.set_xlabel('Factor')
    axes.set_ylabel('Score')
    

# variables
'''
FACTORS = ['Road quality', 'Road surface type', 'Cycle lane type', 'Facilities', 
           'Bike parking', 'Public transport connection', 'Construction']
'''

vicpark = [4, 5, 4, 3, 4, 4, 5]
stheliers = [3, 4, 2, 3, 2, 2, 1]
hurstmere = [2, 3, 4, 3, 3, 3, 3] 
waterfront = [5, 5, 4, 4, 4, 5, 2]
cornwall = [4, 4, 1, 3, 0, 0, 5]
westernsprings = [4, 5, 5, 2, 1, 2, 5] 

print(sum(vicpark))
areas = ['Victoria Park', 'St. Heliers', 'Hurstmere Rd.', 'Waterfront', 'Cornwall Park', 'Western Springs']
scores = [100 - (sum(vicpark) / 35) * 100, 
          100 - (sum(stheliers) / 35) * 100,
          100 - (sum(hurstmere) / 35) * 100,
          100 - (sum(waterfront) / 35) * 100, 
          100 - (sum(cornwall) / 35) * 100,
          100 - (sum(westernsprings) / 35) * 100]

# plot variable scores
fig, ax = plt.subplots(1, figsize=(12, 7))
ax.bar(x=areas, height=scores, color=['green', 'red', 'orange', 
                                      'green', 'red', 'orange'])
plt.xticks(rotation=45)
plt.yticks([0, 20, 40, 60, 80, 100])
plt.title('Deprivation Scores for all Areas of Interest')
ax.set_xlabel('Area of Interest')
ax.set_ylabel('Level of Deprivation (%)')
'''
plt.stackplot(FACTORS, 
              vicpark, 
              stheliers, 
              waterfront, 
              hurstmere,
              cornwall,
              westernsprings, labels=['Victoria Park', 'St. Heliers', 
                                      'Hurstmere Rd.', 'Waterfront', 
                                      'Cornwall Park', 'Western Springs'])
plt.xticks(rotation=45)
plt.title('Stacked Line Plot showing Scores of All Areas of Interest')
ax.set_xlabel('Factor')
ax.set_ylabel('Score')
plt.legend(loc='upper right')
'''




build_map = True

if build_map:
  
    
    
    # get map object
    m = get_map()
    
    # add files to map
    tracks_fg = folium.FeatureGroup('Areas of interest')
    build_track('data/stheliers.gpx', 'St. Heliers', stheliers, tracks_fg)
    build_track('data/hurstmere.gpx', 'Hurstmere Rd.', hurstmere, tracks_fg)
    build_track('data/vicpark.gpx', 'Victoria Park', vicpark, tracks_fg)
    build_track('data/waterfront.gpx', 'CBD Waterfront', waterfront, tracks_fg)
    build_track('data/cornwall.gpx', 'Cornwall Park', cornwall, tracks_fg)
    build_track('data/westernsprings.gpx', 'Western Springs', westernsprings, tracks_fg)
    tracks_fg.add_to(m)
    
    # add photos to map
    # have to manually add coords bc I was too dumb to remember to save location data in camera app
    photos_fg = folium.FeatureGroup('Photos')
    map_photo('data/photos/stheliers/IMG_20210906_073942_1.jpg', (-36.850889, 174.853941), photos_fg)
    map_photo('data/photos/stheliers/IMG_20210906_074056_1.jpg', (-36.850840, 174.855706), photos_fg)
    map_photo('data/photos/stheliers/IMG_20210906_074119_1.jpg', (-36.850561, 174.856602), photos_fg)
    map_photo('data/photos/stheliers/IMG_20210906_074806.jpg', (-36.848898, 174.860755), photos_fg)
    map_photo('data/photos/stheliers/IMG_20210906_074839.jpg', (-36.849307, 174.860401), photos_fg)
    
    map_photo('data/photos/waterfront/IMG_20210906_081003_1.jpg', (-36.844188, 174.771024), photos_fg)
    map_photo('data/photos/waterfront/IMG_20210906_081022_1.jpg', (-36.843784, 174.769361), photos_fg)
    map_photo('data/photos/waterfront/IMG_20210906_081026_1.jpg', (-36.843587, 174.768642), photos_fg)
    map_photo('data/photos/waterfront/IMG_20210906_081051_1.jpg', (-36.843467, 174.768009), photos_fg)
    map_photo('data/photos/waterfront/IMG_20210906_081122_1.jpg', (-36.843029, 174.766293), photos_fg)
    map_photo('data/photos/waterfront/IMG_20210906_081247.jpg', (-36.843303, 174.763723), photos_fg)
    
    map_photo('data/photos/vicpark/IMG_20210906_081524_1.jpg', (-36.847607, 174.756422), photos_fg)
    map_photo('data/photos/vicpark/IMG_20210906_081601.jpg', (-36.848169, 174.755548), photos_fg)
    map_photo('data/photos/vicpark/IMG_20210906_081656.jpg', (-36.848491, 174.753386), photos_fg)
    map_photo('data/photos/vicpark/IMG_20210906_081739_1.jpg', (-36.848049, 174.752828), photos_fg)
    map_photo('data/photos/vicpark/IMG_20210906_082003_1.jpg', (-36.848217, 174.756846), photos_fg)
    
    photos_fg.add_to(m)
    
    folium.LayerControl().add_to(m)
    # save and open map in browser
    m.save('index.html')
    webbrowser.open('index.html')
