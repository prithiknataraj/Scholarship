from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

# Create a Flask application instance

app = Flask(__name__)

# Define a route and a view function
@app.route('/',methods=['POST','GET'])
def hello_world():
    url = 'https://www.collegesearch.in/articles/all-india-scholarship'  # Replace with the URL of the webpage you want to scrape
    class_name = 'MsoNormalTable'     # Replace with the actual class name of the table you want to fetch

    # Step 2: Fetch the HTML content of the webpage
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
    else:
        print(f"Error fetching content. Status code: {response.status_code}")
        exit()

    # Step 3: Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Step 4: Find all tables by class name
    tables = soup.find_all('table', class_=class_name)

    # print(tables)

    # Step 5: Extract and print table contents for each table
    all_data= []
    i= 0

    for table in tables:

        for index, row in enumerate(table.find_all('tr')):
            i+= 1

            row_data = [cell.text.strip() for cell in row.find_all(['th', 'td'])]

            image= "static/img/events-"+ str(index)+ ".jpg"

            row_data.append(image)

            all_data.append(row_data)
            
            if 'Scholarship Name' in row_data:
                SN= i
                # i= 0

            if 'Exam Name' in row_data:
                EN= i
                # i= 0

    # Getting the recent scholarship data.
    Scholarship_data= all_data[SN: EN-1]
    Exam_data= all_data[EN: ]

    # Scholarship_data.insert(0, ['Scholarship Name', 'Eligibility Criteria', 'Scholarship Amount', 'Examination date'])
    # Exam_data.insert(0, ['Exam Name', 'Eligibility Criteria', '	Scholarship Amount', 'Application Dates'])

    
    return render_template('index.html',sd = Scholarship_data, ed= Exam_data)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)