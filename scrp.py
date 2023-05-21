import json
import requests

# GraphQL API endpoint
url = 'https://api.ouedkniss.com/graphql'

# Request payload
payload = {
    'operationName': 'Feed',
    'variables': {
        'mediaSize': 'LARGE',
        'hideStore': False,
        'filter': {
            'page': 1,
            'count': 100,
            'categorySlug': 'accessoires_mode',
            'delivery': 'DELIVERY_AVAILABLE',
            'hasPictures': True
        }
    },
    'query': '''
        fragment AnnouncementMiniContent on Announcement {
            id
            title
            slug
            isFromStore
            store {
                id
                __typename
            }
            store @skip(if: $hideStore) {
                name
                imageUrl
                __typename
            }
            defaultMedia(size: $mediaSize) {
                mediaUrl
                __typename
            }
            userReaction {
                isBookmarked
                isLiked
                __typename
            }
            hasDelivery
            deliveryType
            likeCount
            status
            pricePreview
            priceUnit
            oldPrice
            user {
                id
                __typename
            }
            __typename
        }

        query Feed($filter: SearchFilterInput, $mediaSize: MediaSize = SMALL, $hideStore: Boolean = false) {
            announcementFeed(filter: $filter) {
                announcements {
                    data {
                        ...AnnouncementMiniContent
                        __typename
                    }
                    paginatorInfo {
                        hasMorePages
                        __typename
                    }
                    __typename
                }
                __typename
            }
        }
    '''
}

# Send the request
response = requests.post(url, json=payload)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response content as JSON
    data = response.json()

    # Save the data to a JSON file
    with open('data.json', 'w') as file:
        json.dump(data, file)

    print("Data saved to data.json")
else:
    print(f"Request failed with status code {response.status_code}")
