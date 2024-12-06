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

## Git flow:

Commit changes on main. Make sure to push them.

When your ready to deploy. Checkout prod by double clicking on prod in git graph. Right click main, and select merge. Then push changes (sync). This will add all changes from all commits from the main branch. Then make sure to double click main to check it out again so you dont push to prod. Then go to the prod folder. In git graph press the fetch from remote button in top right. Then pull changes (sync). Then deploy by stopping the current process, and running the deployment script. You may need to `python .\manage.py migrate` if there have been db migrations. Make sure you are using the virtual env.