import flickrapi
from pprint import pprint
import time

# import flickr_credentials
from creds import creds as flickr_credentials

def authenticate():
    # Import keys from flickr_credentials
    api_key = flickr_credentials.api_key
    api_secret = flickr_credentials.api_secret

    return flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')


def UserStream(flickr, extratag, userid):
    result = flickr.photos.search(
        user_id=userid, per_page=500, has_geo=1, sort='date-taken-desc',
        extras=extratag)
    return result


def TextStream(flickr, extratag, textword, starttime):
    result = flickr.photos.search(
        tag=textword, per_page=500, has_geo=1,
        sort='date-taken-desc', extras=extratag, min_upload_date=starttime)
    return result


if __name__ == "__main__":
    etag = '''date_taken, date_upload, owner_name, geo, tags, icon_server,
              original_format, machine_tags, o_dims, path_alias, url_Sq,
              url_t, url_s, url_q, url_m, url_n, url_z, url_c, url_l, url_o,
              description, media, license, last_update, views'''

    starttime = 1000000000  # Epoch time
    chose = "samsung"
    picid = "51051083576"
    earliestpulltime=time.time()-5266800 #Current time- 5,266,800 seconds (2 months)
    flickr = authenticate()
    if len(chose) == 13 and chose[:9].isnumeric() and \
                            chose[9:11] == "@N" and \
                            chose[11:].isnumeric():
        print(f"Finding pictures from user: {chose}")
        resu = UserStream(flickr, etag, chose)
    else:
        print(f"Finding pictures that has {chose} in the tag, title or description")
        if picid.isnumeric():
            print(f"And later than 2 months before the Current time in Unix.")
            datelimit = flickr.photos.getInfo(photo_id=picid)
            starttime = earliestpulltime
            print(f"Which is {starttime}")
        resu = TextStream(flickr, etag, chose, starttime)
    pic = resu['photos']
    pprint(pic)
