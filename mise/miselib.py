import csv
import os.path
from urllib.request import urlopen
from urllib.error import URLError
from shutil import copyfileobj
from datetime import datetime

"""Gets daily fuel prices from Italian MISE website"""

mise_base_url = "https://www.mimit.gov.it/images/exportCSV/"
price_csv_file = "prezzo_alle_8.csv"
stations_csv_file = "anagrafica_impianti_attivi.csv"

"""Data type request"""
TYPE_FUEL = "fuel"
TYPE_STATION = "station"

"""
Fuel price csv metadata
as per https://www.mimit.gov.it/images/stories/documenti/Metadati_05sett22_prezzi_carburanti.pdf
"""
FUEL_DESCRIPTION = 1
FUEL_PRICE = 2
FUEL_EXPERIENCE = 3
FUEL_DATE_UPDATED = 4

EXPERIENCE_SELF_SERVICE = "1"
EXPERIENCE_SERVED = "0"


"""
Fuel stations csv metadata
as per https://www.mimit.gov.it/images/stories/documenti/Metadati_05sett22_prezzi_carburanti.pdf
"""
FACILITY_ID = 0
FACILITY_COMPANY = 1
FACILITY_FLAG = 2
FACILITY_TYPE = 3
FACILITY_NAME = 4
FACILITY_ADDRESS = 5
FACILITY_MUNICIPALITY = 6
FACILITY_PROVINCE = 7
FACILITY_LATITUDE = 8
FACILITY_LONGITUDE = 9


class mise:
    """Download and read data from MISE website."""

    def __init__(self, station_id):
        self.station_id = str(station_id)
        self.station = None
        self.fuels = None
        self.stations_ts = None
        self.price_ts = None
        self.dl_path: str = ""

    def update(self):
        """Updates both prices and stations data from MISE website"""

        # Downloading stations file if necessary
        dl_stations = self.download_csv(stations_csv_file, 30)

        # Downloading price file if necessary
        dl_price = self.download_csv(price_csv_file)

        if dl_stations and dl_price:
            self.stations_ts = self.get_local_csv_ts(stations_csv_file)
            self.price_ts = self.get_local_csv_ts(price_csv_file)

            c = self.get_csv_content(stations_csv_file, self.station_id)
            if not c:
                self.logger("Station id " + self.station_id + " not found")
                return False
            c = c[0]
            s = station_obj()
            s.company = c[FACILITY_COMPANY]
            s.flag = c[FACILITY_FLAG]
            s.plant_type = c[FACILITY_TYPE]
            s.name = c[FACILITY_NAME]
            s.address = c[FACILITY_ADDRESS]
            s.municipality = c[FACILITY_MUNICIPALITY]
            s.province = c[FACILITY_PROVINCE]
            s.latitude = c[FACILITY_LATITUDE]
            s.longitude = c[FACILITY_LONGITUDE]
            self.station = s

            c = self.get_csv_content(price_csv_file, self.station_id)
            ff = []
            for fuel_type in c:
                f = fuel_obj()
                f.station_id = self.station_id
                f.description = fuel_type[FUEL_DESCRIPTION]
                f.price = fuel_type[FUEL_PRICE]
                f.experience = self.get_experience(fuel_type[FUEL_EXPERIENCE])
                f.timestamp = fuel_type[FUEL_DATE_UPDATED]
                ff.append(f)

            self.fuels = ff

        else:
            return False

        return True

    def get_local_csv_ts(self, csv_file):
        """Read local csv file extraction date contained in the first line."""

        if os.path.exists(self.dl_path + csv_file):
            with open(self.dl_path + csv_file, "r") as csvfile:
                first_line = csvfile.readline().strip()
                csv_extraction_date = first_line[-10:]
                ts = datetime.strptime(csv_extraction_date, "%Y-%m-%d")
                return ts

        return False

    def get_csv_content(self, csv_file, station_id):
        """Read csv file provided by MISE website."""

        with open(self.dl_path + csv_file, "r", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=";")
            next(reader)  # Skip header line
            content = []
            for row in reader:
                if row[FACILITY_ID] == station_id:
                    content.append(row)
        return content

    def download_csv(self, csv_file, days_back=1):
        """Download csv only if local file is stale or missing."""

        local_file_ts = self.get_local_csv_ts(csv_file)

        today = datetime.combine(datetime.now(), datetime.min.time())

        if not local_file_ts or (today - local_file_ts).days > days_back:
            self.logger("Downloading file " + csv_file + " from MISE website")
            url = mise_base_url + csv_file
            try:
                f = urlopen(url)
            except URLError:
                self.logger(
                    "Connection error, failed to download "
                    + csv_file
                    + " from MISE website"
                )
                return False

            if f.status != 200:
                self.logger(
                    "MISE website returned an invalid HTTP response " + f.status
                )
                return False

            with open(self.dl_path + csv_file, "wb") as local_file:
                copyfileobj(f, local_file)

        return True

    def get_experience(self, exp_id):
        """Self service or served."""

        if exp_id == EXPERIENCE_SELF_SERVICE:
            return "self"
        elif exp_id == EXPERIENCE_SERVED:
            return "servito"
        else:
            return "sconosciuto"

    def logger(self, msg):
        pass


class station_obj:
    """Station object"""

    def __init__(self):
        self.company = None
        self.flag = None
        self.plant_type = None
        self.name = None
        self.address = None
        self.municipality = None
        self.province = None
        self.latitude = None
        self.longitude = None


class fuel_obj:
    """Fuel object"""

    def __init__(self):
        self.station_id = None
        self.description = None
        self.price = None
        self.experience = None
        self.timestamp = None
