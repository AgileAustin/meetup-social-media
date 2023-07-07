def handler(pd: "pipedream"):
  # Initialize data store that contains event titles that have already been announced
  data_store = pd.inputs["data_store"]
  records = {}
  eventDescription = ""
  eventImage = ""
  keys = data_store.keys()

  # iterate through all keys within the Data Store to generate a new dictionary
  for key in keys:
    records[key] = data_store[key]

  # Get a count of new Meetup events for looping purposes
  try:
    eventCount = pd.steps["code"]["$return_value"]["data"]["self"]["upcomingEvents"]["count"]
  except:
    pd.flow.exit("Did not get a response for events from the Meetup API")

  iterator = range(eventCount)
  allEventRecordsInDataStore = True
# Loop through all events, grabbing the title, URL, and description
  for eventPosition in iterator:
    eventTitle = pd.steps["code"]["$return_value"]["data"]["self"]["upcomingEvents"]["edges"][eventPosition]["node"]["title"]
    eventUrl = pd.steps["code"]["$return_value"]["data"]["self"]["upcomingEvents"]["edges"][eventPosition]["node"]["eventUrl"]
    description = pd.steps["code"]["$return_value"]["data"]["self"]["upcomingEvents"]["edges"][eventPosition]["node"]["description"]
    try:
      eventImageId = pd.steps["code"]["$return_value"]["data"]["self"]["upcomingEvents"]["edges"][eventPosition]["node"]["images"][0]["id"]
      eventImageBaseUrl = pd.steps["code"]["$return_value"]["data"]["self"]["upcomingEvents"]["edges"][eventPosition]["node"]["images"][0]["baseUrl"]
      eventImage = eventImageBaseUrl + eventImageId + "/676x380.jpg"
    except:
      eventImage = ""
      print("Event image does not exist, continuing on without it")

    # Only in the case that we find an event title that has not been announced will we return
    # the event particulars, otherwise, we break out of the flow. Also, we limit to 2700
    # characters due to Slack API limitations.
    if eventTitle not in records["events"]:
      eventDescription = (description[:2700] + '..') if len(description) > 2700 else description
      allEventRecordsInDataStore = False
      break

  if allEventRecordsInDataStore:
    pd.flow.exit("All events have been announced already")

  return eventUrl, eventDescription, eventTitle, eventImage
