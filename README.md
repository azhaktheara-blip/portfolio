# Modern Portfolio — Django + CSV

## Quick Start (Windows)

```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Then open http://127.0.0.1:8000

## Customise

Edit the CSV files in /data/ with any spreadsheet app or text editor:
- data/profile.csv    — your name, bio, links
- data/projects.csv   — your projects
- data/skills.csv     — skill levels (0-100)
- data/experience.csv — work history

Contact form submissions are saved to data/messages.csv
View them at: http://127.0.0.1:8000/admin-messages/

## PythonAnywhere Deployment

1. Upload & extract zip
2. Web app → Manual → Python 3.10
3. Source code: /home/<user>/portfolio_clean
4. WSGI file: set DJANGO_SETTINGS_MODULE to portfolio.settings
5. Install requirements in virtualenv
6. Reload!
