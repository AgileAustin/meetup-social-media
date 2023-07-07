import { axios } from "@pipedream/platform"

export default defineComponent({
  props: {
    meetup: {
      type: "app",
      app: "meetup",
    }
  },
async run({steps, $}) {
    const data = {
      "query": `query {
        self {
          id name upcomingEvents {
            pageInfo {
              startCursor 
            } count edges {
              node {
                title eventUrl description createdAt dateTime
                images {
                  id
                  baseUrl
                  preview
                }
              } 
            } 
          }
        }
      }`
}

    return await axios($, {
      method: "post",
      url: `https://api.meetup.com/gql`,
      headers: {
        Authorization: `Bearer ${this.meetup.$auth.oauth_access_token}`,
      },
      data,
    })
  },
})
