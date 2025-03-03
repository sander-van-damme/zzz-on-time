# Zzz on Time (Beeminder + Garmin Connect)
Log your Garmin Connect sleep data to Beeminder.

## How to use
1. Clone this repository.
2. `python -m pip install -r requirements.txt`
3. Set the variables in the `.env` file.
4. Log in to Garmin: `python login.py`
3. Create a cronjob that runs `python main.py` daily. Probably somewhere in the afternoon, giving your watch some time to synchronize last night's data.

## Quirks
- It currently doesn't work if your regular bedtime is past midnight.

## Thanks to
- [garth](https://github.com/matin/garth)
- [Beeminder](https://www.beeminder.com/)
- [Garmin Connect](https://connect.garmin.com/)
