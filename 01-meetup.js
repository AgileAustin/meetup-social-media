import { axios } from "@pipedream/platform";

export default defineComponent({
  props: {
    meetup: {
      type: "app",
      app: "meetup",
    },
  },
  async run({ steps, $ }) {
    const data = {
      query: `query {
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
      }`,
    };

    let response = null;
    let retries = 3;

    while (retries > 0) {
      response = await axios($, {
        method: "post",
        url: `https://api.meetup.com/gql`,
        headers: {
          Authorization: `Bearer ${this.meetup.$auth.oauth_access_token}`,
        },
        data,
      });

      if (response !== null) {
        break;
      }

      retries--;
    }

    return response;
  },
});
