import json
import requests
from tqdm import tqdm

# GraphQL API endpoint
url = 'https://api.ouedkniss.com/graphql'

# Request payload
payload = {
    'operationName': 'Feed',
    'variables': {
        'mediaSize': 'SMALL',
        'hideStore': False,
        'filter': {
            'page': 1,
            'count': 12,
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

announcements = []  # To store all the announcements

# Send the initial request to get the first page
response = requests.post(url, json=payload)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    announcement_data = data['data']['announcementFeed']['announcements']['data']
    announcements.extend(announcement_data)

    # Check if there are more pages
    has_more_pages = data['data']['announcementFeed']['announcements']['paginatorInfo']['hasMorePages']
    page_count = 1

    # Paginate through the results until there are no more pages
    while has_more_pages:
        # Increment the page number
        payload['variables']['filter']['page'] += 1

        # Send the next request
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            data = response.json()
            announcement_data = data['data']['announcementFeed']['announcements']['data']
            announcements.extend(announcement_data)

            has_more_pages = data['data']['announcementFeed']['announcements']['paginatorInfo']['hasMorePages']
            page_count += 1
        else:
            print(f"Request failed with status code {response.status_code}")
            break

    # Initialize the progress bar
    progress_bar = tqdm(total=page_count, unit='page', bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}')

    # Reset the page number in the payload
    payload['variables']['filter']['page'] = 1

    # Send requests again to update the progress bar
    for _ in range(page_count):
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            data = response.json()
            announcement_data = data['data']['announcementFeed']['announcements']['data']
            announcements.extend(announcement_data)

            # Update the progress bar
            progress_bar.update(1)
        else:
            print(f"Request failed with status code {response.status_code}")
            break

    # Close the progress bar
    progress_bar.close()

    # Save the data to a JSON file
    with open('data.json', 'w') as file:
        json.dump(announcements, file)

    print("Data saved to data.json")
else:
    print(f"Request failed with status code {response.status_code}")
