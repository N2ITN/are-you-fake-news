import gmplot

from mongo_ip import db


def get_coords():
    return db['ip_logs'].aggregate([{
        "$group": {
            "_id": {
                "latitude": "$latitude",
                "longitude": "$longitude"
            }
        }
    }])


def clean_coords(raw):
    yield from list(zip(*[list(_.values())[0].values() for _ in raw]))


def plot(coords):
    lat, lon = coords
    gmap = gmplot.GoogleMapPlotter(0, 0, 2.5, apikey='AIzaSyD3trg2UkFJO-n67Z4MOwB7Ft4J66aFJEI')
    gmap.heatmap(lat, lon)
    gmap.draw("./templates/mymap.html")


def run():

    plot(clean_coords(get_coords()))


if __name__ == '__main__':
    run()