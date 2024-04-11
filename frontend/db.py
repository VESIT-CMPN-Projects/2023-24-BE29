import sqlite3

class GetCarDetails():
    # def __init__(self) -> None:
    #     pass

    def get_last_number_plate(self):
        try:
            # Connect to the database
            conn = sqlite3.connect('Frontend/Databases/car_data.db')
            c = conn.cursor()

            # Execute a SELECT query to get the last row ordered by id in descending order
            c.execute('SELECT number_plate FROM cars ORDER BY id DESC LIMIT 1')
            result = c.fetchone()

            if result:
                last_number_plate = result[0]
                return last_number_plate
            else:
                print("No records found in the table.")
                return None

        except sqlite3.Error as e:
            print("Error occurred while retrieving data from the database:", e)
            return None

        finally:
            # Close the database connection
            conn.close()

    def get_last_color(self):
        try:
            # Connect to the database
            conn = sqlite3.connect('Frontend/Databases/car_data.db')
            c = conn.cursor()

            # Execute a SELECT query to get the last row ordered by id in descending order
            c.execute('SELECT color FROM cars ORDER BY id DESC LIMIT 1')
            result = c.fetchone()

            if result:
                last_color = result[0]
                return last_color.lower()
            else:
                print("No records found in the table.")
                return None

        except sqlite3.Error as e:
            print("Error occurred while retrieving data from the database:", e)
            return None

        finally:
            # Close the database connection
            conn.close()

    def get_last_model(self):
        try:
            # Connect to the database
            conn = sqlite3.connect('Frontend/Databases/car_data.db')
            c = conn.cursor()

            # Execute a SELECT query to get the last row ordered by id in descending order
            c.execute('SELECT model FROM cars ORDER BY id DESC LIMIT 1')
            result = c.fetchone()

            if result:
                last_model = result[0]
                return last_model.lower()
            else:
                print("No records found in the table.")
                return None

        except sqlite3.Error as e:
            print("Error occurred while retrieving data from the database:", e)
            return None

        finally:
            # Close the database connection
            conn.close()
