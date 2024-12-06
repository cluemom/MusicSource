# Music Source

This project was built on and for Windows. 

## Getting Started

1. Make sure you have python installed :)

2. Create a virtual environment `python -m venv venv`. and make sure the environment is active. `.\venv\Scripts\activate`

3. Install dependencies `pip install -r .\requirements.txt`

4. Copy `example.env` to `.env` and set the proper values

If running into problems with the postgres plsycop package, refer to: `https://www.psycopg.org/psycopg3/docs/basic/install.html#`

### Local testing

Run the app for local testing using `python .\manage.py runserver`. Make sure you run it in your virtual environment  `.\venv\Scripts\activate`.

### Producton and Deployment

Make sure to set important security values in your .env
