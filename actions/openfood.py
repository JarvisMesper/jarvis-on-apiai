from actions.RequestOpenFood import RequestOpenFood
from actions.RequestOpenFood import ProductBuilder


def getOpenFoodInfo(req):
    print (req)
    
    result = req.get("result")
    parameters = result.get("parameters")
    barcode = parameters.get("productBarCode")

    data = {}

    if barcode:
        try:
            res = RequestOpenFood.get_product(barcode=barcode)
            #res = ProductBuilder.clean_data(res)
            data["info"] = res
        except:
            data["info"] = "Can't find this product on the OpenFood database"

    return data
    


def makeProductInfoWebhookResult(req):
    data = getOpenFoodInfo(req)
    if data is None:
        return {}

    if data.get("info") is None:
        return {}

    info = data.get("info").get("_source")


    speech = info.get("name_en")
    if speech is None:
        speech = info.get("name_fr")
    if speech is None:
        speech = info.get("name_ge")
    if speech is None:
        speech = info.get("name_it")


    print("Response:")
    print(speech)



    images = info.get("images")[0]
    if images is not None:
        images_data = images.get("data")
        if images_data is not None:
            images_thumb = images_data.get("thumb")
            if images_thumb is not None:
                image_url = images_thumb.get("url")

    if image_url is None:
        print("Can't find image url")
        image_url = ""
    else:
        print("Image URL:")
        print(image_url)

    return {
        "speech": speech,
        "displayText": speech,
        "data": {
            "facebook": {
                "attachment": {
                    "type":"template",
                    "payload":{
                        "template_type":"generic",
                        "elements":[
                           {
                            "title":speech,
                            "image_url":image_url,
                            "subtitle":"From OpenFood.ch",
                            "default_action": {
                              "type": "web_url",
                              "url": "https://openfood.ch",
                              "messenger_extensions": true,
                              "webview_height_ratio": "tall"
                            }     
                          }
                        ]
                    }
                }
            }
        },
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample",
        
    }