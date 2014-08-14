Satellite Pies
==============

<a href="https://www.flickr.com/photos/hugovk/13686739945" title="Satellite Pies by hugovk, on Flickr"><img src="https://farm3.staticflickr.com/2904/13686739945_09d28d390b_c.jpg" width="800" height="500" alt="Satellite Pies"></a>

A hacked up Python version of [Satellite Eyes](http://satelliteeyes.tomtaylor.co.uk/) for Windows to set your desktop wallpaper to a map of your current position.
You can use maps from [OpenStreetMap](www.openstreetmap.org), [Stamen's Watercolor and Toner](maps.stamen.com), [MapQuest Open Aerial](http://developer.mapquest.com/web/products/open/map), or another [slippy map tile server](http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames).

Usage
-----

```
usage: satellite_pies.py [-h] [-t {toner,watercolor,osm,aerial}] [-u URL]
                         [-z level] [-x lat,lon] [-n NAME] [-r] [-w minutes]

Satellite pies.

optional arguments:
  -h, --help            show this help message and exit
  -t {toner,watercolor,osm,aerial}, --tile {toner,watercolor,osm,aerial}
                        Type of map tile to use (default: watercolor)
  -u URL, --url_base URL
                        Base URL for map tiles (use instead of --tile)
                        (default: None)
  -z level, --zoom level
                        Map zoom level (default: None)
  -x lat,lon, --coords lat,lon
                        Instead of your current position, use these
                        coordinates (default: None)
  -n NAME, --name NAME  Instead of your current position, use this place name
                        (default: None)
  -r, --repeat          Repeat (default: False)
  -w minutes, --wait minutes
                        Minutes to wait between repeat (default: 5)

```

Examples
--------

Run once with Watercolor maps at zoom 17:

    satellite_pies.py

Run once with Toner maps at zoom 15:

    satellite_pies.py --tile toner --zoom 15

Update every ten minutes with OpenStreetMap maps:

    satellite_pies.py --tile osm --repeat --wait 10

Run once with an aerial map of a specific location (remembering west is negative):

    satellite_pies.py -x 38.8977,-77.0366 --tile aerial

Show an aerial photo of a named place:

    satellite_pies.py -t aerial -n "golden gate bridge"

Show a map of a named place with a specified map tile server:

    satellite_pies.py --name copenhagen --url_base http://tile.stamen.com/toner-lite

Prerequisites
-------------

*Python*

 * [Pillow](http://pillow.readthedocs.org/en/latest/) or [PIL](http://www.pythonware.com/products/pil/)
 * [OSM Viz](http://cbick.github.com/osmviz/html/index.html)
 * For --repeat, [Twisted](http://twistedmatrix.com/trac/)

Install with pip:

`pip install -r requirements.txt`

*Optional prerequisite for Windows XP*

 * Windows XP needs [WirelessNetConsole](http://www.nirsoft.net/utils/wireless_net_console.html) to get a list of nearby wifi networks, otherwise it will be based on your public-facing IP address which is less accurate.

 * For Windows Vista, Windows 7 and Windows Server 2008, nearby wifi networks can be found with `netsh wlan` (not available on XP).

Map terms of use
----------------

The map images have the following terms of use.

 * OSM maps: (c) [OpenStreetMap](http://wiki.openstreetmap.org/wiki/Tile_usage_policy) and contributors, [CC-BY-SA](http://creativecommons.org/licenses/by-sa/3.0/).

 * Watercolor and Toner maps: Courtesy of [Stamen Design](http://maps.stamen.com/), and use OpenStreetMap data, (c) [OpenStreetMap](http://wiki.openstreetmap.org/wiki/Tile_usage_policy) and contributors
[CC-BY-SA](http://creativecommons.org/licenses/by-sa/3.0/).

 * MapQuest Open Aerial Tiles: Portions Courtesy NASA/JPL-Caltech and U.S. Depart. of Agriculture, Farm Service Agency. Tiles Courtesy of [MapQuest](http://developer.mapquest.com/web/products/open/map#terms).
