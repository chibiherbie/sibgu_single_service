"""POST
https: // qtickets.ru / api / rest / v1 / clients
Accept: application / json
Cache - Control: no - cache
Content - Type: application / json
Authorization: Bearer
TOKEN

{
    "data": {
        "email": "vasilev@gmail.com",
        "details": {
            "name": "Василий",
            "surname": "Васильев"
        }
    }
}

"""
import json

import requests

data = { "email": "bekkerrdm@gmail.com",
        "details": {
           "name": "Василий",
          "surname": "Васильев"
    }}

a = requests.get('https://qtickets.ru/api/rest/v1/events/52323', headers={"Accept": "application/json", "Cache-Control": "no-cache", "Content-Type": "application/json", "Authorization": 'Bearer fwvvCW4jCLwi9YQXp4hGT8dMOTjtz6Le'})
print(a.content)
g = a.json()
print(g)

data = {
    "event_id": 52323,
    # "backend": True,
    # "backend_sign": "eyJpdiI6Im5wY0I0ZFFsMVZLdTJXazkrQWVhaEE9PSIsInZhbHVlIjoiK2hUa25sc1RVY2Q1OFgrMDE4WVNMbnVneVRXc045UkRYUEVWUnViN3h5YzBIZ1ZqXC9Nb3BYakF3NjdlUUdHMG1pa1NGNFwvQlNHY1ZNV3VVUVIzUWtcL2VaMzB6ODBOS0t2a1MrWkg2NjFBNGZCbWtVVmxPcDJrMFpHYmZVenBSdkdKWUpaY2VFRUZEeUY1aTlrTEdGUE9La3o0NUVmR3dCb09qNUZmbmtMdkEwPSIsIm1hYyI6ImZlYTQyNDVlMzM3OWMxMDJkMGM5ODY3ODU5MDI1MDU5NzMzN2M3Mzg2OWEyZjE4ZTNmODhmNDQ4ODRlYTg5MmIifQ==",
    "lang": "ru",
    "height": 645,
    # "kkmserver_installed": None,
    # "hide_poster": 1,
    "widget_session": "HcvuHF6OS3e1h1PaBNZ0W6AmTXXXaDwtIN8nlXVu",
    "__qtickets_session": "GyF80fSeZUFD9TfrOpcmbBCu301pncrQGNX5T0ND",
    "container_width": 960,
    "integrations[googleanalytics][trackingId]": "UA-32309773-1",
    "integrations[googleanalytics][clientId]": "1982360222.1665495927",
    "handlers": "resizeHeight|fixIframeSize|loadShow|loadEvent|loadOrganizer|systemComplete|appSlide|setVar|basketTotalSystem|createOrder|resizeDisableAll|resizeEnableAll|InAppBrowser|extendInstanceRequest|complete|error|backendAfterCreateOrder",
    "referer": "https://sibhub.qtickets.ru/",
    "form_settings[payload]": "H4sIAAAAAAAAA+1UwU4CMRD9FdMzB1gRWH7FmE27HZaG3XZpS0gkmyhnj55M/AdigqIC/kL3j+zCKgsU49XESw/vvZn3ZibpBClQigkeMIq6iABthKTXpISShkcb1K+Df9HBPvF6Lf+8g9u90PO9Fqoh1RfjTZHX9s69Zg1JGI6YhIDjBFC3vgPSvuBbJIwZcK0CBVozHinUnaDUKiRETGmJdREEOCYxFGnq1ibFUrOQpZjrA2bfbw8qHfcwISPM2fXWw1EzFnIQpEKxQnDAhSJJbHBHpC8FJJjFP/AVQxddDeziT4V3aV2DuHSnhyI4HACnAWWqWHipEJJFjOP4/2h/5mhZDcWYR8XFHGEmliRQLMA8mpl5MU/2XZmFmZ+ZN7M2S/NRAovCK8Yh9EVMQf6qwnofDFXxu7fid/Nspev8Np/md8cGxxLb8Xv8Sq+HjfHSzM0qn5pZfmPtX4/7uWVZVna1WxmOQBVJ7bd0eVVDBKsB6EM0HCktkqDHIKYlVL3CDs8+ASj4r7dbBQAA",
    "form_settings[hash]": "dc8245a18276a2651f56e0878dfa6c18",
    "log[settings][email]": "bekkerrdm@gmail.com",
    "log[settings][phone]": "",
    "log[request][email]": "",
    "log[request][phone]": "",
    "client_email": "bekkerrdm@gmail.com",
    "payment_type_id": "25608-0",
    "check_price[]": "0 руб.",
    "check_price[]": ""
}

b = requests.post('https://sibhub.qtickets.ru/widget/create-order?cache_lock_key=GyF80fSeZUFD9TfrOpcmbBCu301pncrQGNX5T0ND', data=data)
print(b.content)