import requests
from bs4 import BeautifulSoup
import json

departments={}

def handle_html_tags(html):
    html_string=html
    soup = BeautifulSoup(html_string, 'html.parser')
    text_list = []

    # Find all <li> elements and extract their text
    li_elements = soup.find_all('li')
    for li in li_elements:
        text_list.append(li.get_text())

    return text_list

def extract_all_element_job(url):

    response = requests.get(url)

    if response.status_code == 200:
        content = response.json()

        #how to indentify job departments and also i doing hardcode for this job id because that department it self is there in carrer page due that also not there in html structure.
        if content['id']!="743999906322434":
            dept_val=content['department']['label']


        #how to indentify job title
        title=content['name']

        #how to indentify job location
        location=content['location']['city']+','+content['customField'][-1]['valueLabel']

        #how to indentify Job Description
        Job_Description=content['jobAd']['sections']['jobDescription']['text']
        Job_Description=handle_html_tags(Job_Description)

        #how to indentify Job qualifications
        Job_qualifications=content['jobAd']['sections']['qualifications']['text']
        Job_qualifications=handle_html_tags(Job_qualifications)

        #how to indentify Job type
        typeOfEmployment=content['typeOfEmployment']['label']

        job = {
        'title': title,
        'location': location,
        'description':Job_Description ,
        'qualification': Job_qualifications,
        'job_type': typeOfEmployment
        }

        #how to indentify job departments
        if content['id']!="743999906322434":
            dict_key=str(content['department']['label'])
            if dict_key not in departments:
                departments[dict_key]=[]
                departments[dict_key].append(job)
            else:
                departments[dict_key].append(job)
                
        return departments

    else:
        print("Error: Unable to fetch content from the URL")

# Main function to scrape all departments and jobs
def scrape_all_jobs():
    base_url = 'https://www.cermati.com/karir/lowongan'
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the script tag with id="initials" and type="application/json"
    script_tag = soup.find('script', id='initials', type='application/json')

    # Get the content of the script tag
    script_content = script_tag.string

    # Parse the JSON content
    json_data = json.loads(script_content)

    href_value = json_data['smartRecruiterResult']['content']

    job_links=[]

    for i in range(len(href_value)):
        job_links.append(href_value[i]['ref'])
        res=extract_all_element_job(href_value[i]['ref'])
    
    file_path = "solution.json"
    # Write the dictionary variable to a JSON file
    with open(file_path, 'w') as json_file:
        json.dump(res, json_file)

    print("JSON file created successfully.")

# Start scraping
scrape_all_jobs()

