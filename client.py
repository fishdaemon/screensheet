import requests, json

def convert_markdown(name, markdown_file_path, api_url):
    with open(markdown_file_path, 'r') as file:
        markdown_content = file.read()

    data = {
        'name': name,
        'markdown': markdown_content
    }

    response = requests.post(api_url, data=data)
    if response.status_code == 200:
        print(f"{json.dumps(response.json(), indent=4)}")
        #json_response = response.json()
        #print(f"{json_response}")
    else:
        print(f"Error occurred: {response.text}")

if __name__ == '__main__':
    api_url = 'http://localhost:5000/api/embedding'
    markdown_file_path = 'crawler/a-proclamation-on-flag-day-and-national-flag-week-2023.md'
    name = 'a-proclamation-on-flag-day-and-national-flag-week-2023'

    convert_markdown(name, markdown_file_path, api_url)