import requests
import urllib.request
from io import BytesIO
from PIL import Image

def handler(pd: "pipedream"):
  commentaryEscaped = ""
  staticPostTextBeginning = "We just posted another Agile Austin event on our Meetup page, "
  staticPostTextMiddle = "You can sign up at the link below!\n\n"
  staticPostTextEnd = "Topic description:\n\n"
  signUpLink = pd.steps["Python_Compare_Meetup_To_Data_Store"]["$return_value"][0]
  description = pd.steps["Python_Compare_Meetup_To_Data_Store"]["$return_value"][1]
  meetupTitle = pd.steps["Python_Compare_Meetup_To_Data_Store"]["$return_value"][2]
  meetupImage = pd.steps["Python_Compare_Meetup_To_Data_Store"]["$return_value"][3]
  print("meetup image: " + meetupImage)
  token = f'{pd.inputs["linkedin"]["$auth"]["oauth_access_token"]}'
  commentary = staticPostTextBeginning + "\"" + meetupTitle + ".\" " + staticPostTextMiddle + signUpLink + "\n\n" + staticPostTextEnd + description

  special_chars = ["{", "}", "@", "[", "]", "(", ")", "<", ">", "#", "*", "_", "~"]
  escaped_string = ""

  for char in commentary:
    if char in special_chars:
      commentaryEscaped += "\\" + char
    else:
      commentaryEscaped += char
  print(commentaryEscaped)

  authorization = f'Bearer {token}'
  headers = {
    "Authorization": authorization,
    "Content-Type": "application/json",
    "User-Agent": "pipedream/1",
    "LinkedIn-Version": "202304"
  }

  def initializeImageUpload():
    imageInitialization = {
      "initializeUploadRequest": {
        "owner": "urn:li:organization:3707917"
      }
    }
    imageUploadRequest = requests.post('https://api.linkedin.com/rest/images?action=initializeUpload', headers=headers, json=imageInitialization)
    imageUploadRequestResponse = imageUploadRequest.json()
    uploadUrl = imageUploadRequestResponse["value"]["uploadUrl"]
    imageLink = imageUploadRequestResponse["value"]["image"]
    print(imageLink)
    return(uploadUrl, imageLink)
 
  def uploadImage(imageInitilizationResults):
    # Open the image from the URL using the PIL library
    response = requests.get(meetupImage)
    image = Image.open(BytesIO(response.content))
    # Convert the image to bytes
    image_bytes = BytesIO()
    image.save(image_bytes, format='JPEG')
    image_data = image_bytes.getvalue()
    imageHeaders = {
      "Authorization": authorization,
      "Content-Type": "application/jpeg",
      "User-Agent": "pipedream/1",
      "LinkedIn-Version": "202304"
    }
    imageUploadResponse = requests.put(imageInitilizationResults[0], headers=imageHeaders, data=image_data)

  if meetupImage != "":
    imageInitilizationResults = initializeImageUpload()
    uploadImage(imageInitilizationResults)
    data = {
      "author": "urn:li:organization:3707917",
      "commentary": commentaryEscaped,
      "visibility": "PUBLIC",
      "lifecycleState": "PUBLISHED",
      "distribution": {
        "feedDistribution": "MAIN_FEED",
        "targetEntities": [],
        "thirdPartyDistributionChannels": []
        },
        "content": {
          "media": {
            "title":"title of the video",
            "id": imageInitilizationResults[1]
        }
      }
    }
  else:
    data = {
      "author": "urn:li:organization:3707917",
      "commentary": commentaryEscaped,
      "visibility": "PUBLIC",
      "lifecycleState": "PUBLISHED",
      "distribution": {
        "feedDistribution": "MAIN_FEED",
        "targetEntities": [],
        "thirdPartyDistributionChannels": []
      }
    }
  
  r = requests.post('https://api.linkedin.com/rest/posts', headers=headers, json=data)
  print(r)
