import requests

# Set the API endpoint
url = 'https://graphql.anilist.co'

# Set the query and variables
def search_anime(title):
    query = '''
    query ($search: String) {
        Page {
            media(search: $search, type: ANIME) {
                id
                title {
                    romaji
                }
                startDate {
                    year
                    month
                    day
                }
            }
        }
    }
    '''

    variables = {
        'search': title,
        'page': 1 # Set the page to 1 to only get results from the first page
    }

    response = requests.post(url, json={'query': query, 'variables': variables})

    if response.status_code == 200:
        data = response.json()['data']['Page']['media']
        return data
    else:
        print(f"Error: {response.status_code}")
        return None

def search_by_id(id):
    query = '''
    query ($id: Int) {
      Media (id: $id, type: ANIME) {
        title {
          romaji
        }
        coverImage {
          extraLarge
        }
        startDate {
          year
        }
        description
      }
    }
    '''
    variables = {
        'id': id  # Replace with the ID of the anime you want to search for
    }

    # Send the API request
    response = requests.post(url, json={'query': query, 'variables': variables})

    # Extract the data from the API response
    if response.status_code == 200:
        data = response.json()['data']['Media']
        return data
    else:
        print(f"Error: {response.status_code}")
        return None

    # # Print the extracted data
    # print(f"Title (romaji): {data['title']['romaji']}")
    # print(f"Image URL: {data['coverImage']['extraLarge']}")
    # print(f"Year: {data['startDate']['year']}")
    # print(f"Description: {data['description']}")


# search_results = search_anime('Naruto')
# print(search_results)
# for anime in search_results:
#     start_date = anime["startDate"]
#     formatted_date = f"{start_date['day']:02}/{start_date['month']:02}/{start_date['year']}"
#     print(f"{anime['id']}, {anime['title']['romaji']}, {formatted_date}")
