import os
from datetime import datetime, timedelta
import csv
import uuid

class FileManager:

    def __init__(self):
        self.__data_in = {}
        self.__script_dir = os.path.dirname(__file__)
        self.__days_dir = os.path.join(self.__script_dir, "days.csv")
        self.__active_dir = os.path.join(self.__script_dir, "variables/active")
        self.__inactive_dir = os.path.join(self.__script_dir, "variables/inactive")
        self.__export_dir = os.path.join(self.__script_dir, "export")
    
    def get_days_file(self):
        return self.__days_dir
    
    def get_variables(self, active=True):
        if active:
            return [name.split(".")[0] for name in os.listdir(self.__active_dir)]
        else:
            return [name.split(".")[0] for name in os.listdir(self.__inactive_dir)]
    
    def get_options(self, name):
        var_dir = self.find_variable(name)

        if var_dir == None:
            return
        
        with open(var_dir) as var_file:
            first_line = var_file.readline()

        options = first_line.split(",")
        options.pop(0)

        if len(options) != 0:
            options[-1] = options[-1].strip()

        return options
    
    def add_variable(self, name: str, categories = []):

        filename = name + ".csv"

        variable_path = os.path.join(self.__active_dir, filename)

        with open(variable_path, "a") as new_variable:
            new_variable.write("ID")

            for category in categories:
                new_variable.write("," + category)

            new_variable.write("\n")
    
    def find_variable(self, name):

        filename = name + ".csv"

        active_list = os.listdir(self.__active_dir)
        inactive_list = os.listdir(self.__inactive_dir)

        if filename in active_list:
            file_dir = os.path.join(self.__active_dir, filename)
        elif filename in inactive_list:
            file_dir = os.path.join(self.__inactive_dir, filename)
        else:
            return
        
        return file_dir
    
    def move_variable(self, name: str):
        
        filename = name + ".csv"

        active_list = os.listdir(self.__active_dir)
        inactive_list = os.listdir(self.__inactive_dir)

        old_dir = self.find_variable(name)

        if filename in active_list:
            new_dir = os.path.join(self.__inactive_dir, filename)
        elif filename in inactive_list:
            new_dir = os.path.join(self.__active_dir, filename)
        else:
            return
        
        os.rename(old_dir, new_dir)
    
    def rename_variable(self, cur_name: str, new_name: str):
        cur_dir = self.find_variable(cur_name)

        if cur_name in self.get_variables(True):
            new_dir = os.path.join(self.__active_dir, new_name + ".csv")
        else:
            new_dir = os.path.join(self.__inactive_dir, new_name + ".csv")

        

        os.rename(cur_dir, new_dir)
    
    def check_variable(self, name: str):
        file_dir = self.find_variable(name)

        if file_dir == None:
            return
        
        with open(file_dir) as var_file:
            count = -1 # not counting the header
            for line in var_file:
                if count > 100:
                    return ">100"
                count += 1
            else:
                return count      
    
    def delete_variable(self, name: str):
        file_dir = self.find_variable(name)

        if file_dir == None:
            return

        os.remove(file_dir)
    
    def export(self, name):
        filename = name + ".csv"
        file_dir = os.path.join(self.__export_dir, filename)
        with open(self.get_days_file(), "r") as day_file, open(file_dir, "a") as export_file:

            export_file.write("date")
            
            for var in self.get_variables():
                export_file.write("," + var)
            
            export_file.write("\n")

            next(day_file) # skipping the head
            for day in day_file:
                day_data = day.strip().split(",")
                export_file.write(day_data[1])


                for var in self.get_variables():
                    var_dir = self.find_variable(var)
                    with open(var_dir, "r") as var_file:

                        next(var_file) # skipping the head
                        for line in var_file:
                            var_data = line.strip().split(",")
                            if var_data[0] == day_data[0]:
                                export_file.write("," + var_data[1])
                                break
                        else:
                            export_file.write("," + "NA")
                
                export_file.write("\n")

                



    
    
class Interface:
    def __init__(self):
        self.__manager = FileManager()
        self.__cur_date = datetime.today()
        self.__date_format = "%d.%m.%Y"
    
    def clear(self, word: str):

        if word == "#":
            return word

        allowed = "abcdefghijklmnopqrstuvwxyz1234567890_"

        word = word.strip().lower()
        word = word.replace(" ", "_")

        for char in word:
            if not char in allowed:
                word = word.replace(char, "@")

        word = word.replace("@", "")

        return word
    
    def input_command(self, message: str, options: tuple):

        while True:
            response = self.clear(input(message))

            if response == "#":
                return response

            if not response in options:
                print("Invalid input")

                expected = ""

                for option in options:
                    expected += option + ", "
                
                expected = expected[0: len(expected) - 2]

                print("Expected input: ", expected)
                continue

            print()
            return response
    
    def input_name(self, message: str):
        while True:
            response = self.clear(input(message))

            if response == "#":
                return response

            if response == "":
                print("Invalid input, special characters are not allowed")
                continue
            
            break

        print()
        return response
    
    def input_num(self, message: str, int_expected = True):
        while True:
            if int_expected:
                try:
                    response = input(message)
                    if response == "#":
                        return response
                    response = int(response)
                    break
                except:
                    print("Invalid input, a whole number is expected")
            else:
                try:
                    response = input(message)
                    if response == "#":
                        return response
                    response = float(response)
                    break
                except:
                    print("Invalid input, a number is expected")
        
        print()
        return response    
    
    def input_date(self, message: str):
        while True:
            date_str = input(message)

            if date_str == "#":
                return date_str

            try:
                date = datetime.strptime(date_str, self.__date_format)
            except:
                print("invalid input, input the date in the following format: dd.mm.yyyy")
                continue

            break

        print()
        return date

    def print_variables(self):

        active = self.__manager.get_variables(True)
        inactive = self.__manager.get_variables(False)

        print("ACTIVE:")
        print()

        for var in active:
            print(var)
        
        print()

        print("INACTIVE:")
        print()

        for var in inactive:
            print(var)
        
        print()

        pass

    def add_variable(self):

        while True:
            name = self.input_name("name: ")

            if name == "#":
                return name


            if self.__manager.find_variable(name) == None:
                break
            else:
                print("Variable with this name already exists")

        var_type = self.input_command("1 - Numeric, 2 - Categorical: ", ("1", "2"))

        if var_type == "#":
            return var_type

        if var_type == "1":
            categories = []
        else:
            category_num = self.input_num("Number of categories: ")

            if category_num == "#":
                return category_num

            categories = []

            for i in range(0, category_num):
                category = self.input_name(f"Category {i + 1}: ")

                if category == "#":
                    return category

                categories.append(category)
        
        self.__manager.add_variable(name, categories)

    def move_variable(self):
        while True:
            name = self.input_name("name: ")

            if name == "#":
                return name


            if self.__manager.find_variable(name) == None:
                print("variable not found")
            else:
                break
        
        self.__manager.move_variable(name)
    
    def rename_variable(self):
        while True:
            cur_name = self.input_name("current name: ")

            if cur_name == "#":
                return cur_name


            if self.__manager.find_variable(cur_name) == None:
                print("variable not found")
            else:
                break
            
        new_name = self.input_name("new name: ")

        if new_name == "#":
            return new_name

        self.__manager.rename_variable(cur_name, new_name)

    def delete_variable(self):
        while True:
            name = self.input_name("name: ")
            if name == "#":
                return name

            if self.__manager.find_variable(name) == None:
                print("variable not found")
            else:
                break
        
        count = self.__manager.check_variable(name)

        if count == 0:
            warn = ""
        elif count == ">100":
            warn = "more than 100"
        else:
            warn = str(count)

        if warn != "":
            confirm = self.input_command("This variable has " + warn + " entries, are you sure you want to delete it? 1 - yes, 0 - no: ", ("1", "0"))
            if confirm == "0" or confirm == "#":
                return
        
        self.__manager.delete_variable(name)
        
    def manage_variables(self):
        while True:
            self.update_screen()
            self.print_variables()
            command = self.input_command("1 - Add a variable, 2 - (in)activate a variable, 3 - Rename a variable, 4 - Delete a variable: ", ("1", "2", "3", "4"))
            if command == "1":
                self.add_variable()
            elif command == "2":
                self.move_variable()                 
            elif command == "3":
                self.rename_variable()
            elif command == "4":
                self.delete_variable()
            else:
                break

    def update_screen(self):
        os.system("clear")
        os.system("clear")

        date = self.__cur_date.strftime("%d.%m.%Y")

        print("# - Main menu")

        print(len(date) * "=")
        print(date)
        print(len(date) * "=")

    def choose_date(self):
        date = self.input_date("date: ")

        if date == "#":
            return date

        self.__cur_date = date

    def add_entry(self):
        entry = {}
        active_variables = self.__manager.get_variables()

        found = None

        with open(self.__manager.get_days_file(), "r") as day_file:
            for line in day_file:
                try:
                    if line.split(",")[1].strip() == self.__cur_date.strftime(self.__date_format):
                        found = line.split(",")[0]
                except:
                    break

        if found != None:
            print("an entry for this date already exists")
            input("press enter to continue")
            return

            # command = self.input_command("an entry for this date already exists, do you want to rewrite the entry? 1 - yes, 0 - no")

            # if command == "0":
            #     return
            
        for variable in active_variables:
            options = self.__manager.get_options(variable)

            if len(options) == 0:
                inp = self.input_num(variable + ": ", int_expected=False)

                if inp == "#":
                    return inp

                entry[variable] = inp
            else:
                inp = self.input_command(variable + ": ", options)

                if inp == "#":
                    return inp

                entry[variable] = inp


        cur_id = uuid.uuid4()
        
        with open(self.__manager.get_days_file(), "a") as day_file:
            day_file.write(str(cur_id) + "," + self.__cur_date.strftime(self.__date_format) + "\n")
        
        for variable in entry:
            with open(self.__manager.find_variable(variable), "a") as var_file:
                var_file.write(str(cur_id) + "," + str(entry[variable]) + "\n")
        
        self.__cur_date = self.__cur_date + timedelta(days=1)
        
    def export(self):
        name = self.input_name("name of the export file: ")
        self.__manager.export(name)
        print("the data was exported as a " + name + ".csv" + " file")
        input("press enter to continue")

        


    def execute(self):

        while True:
            

            self.update_screen()

            command = self.input_command("1 - Add an entry, 2 - Choose date, 3 - Manage variables, 4 - Export data: ", ("1", "2", "3", "4"))

            if command == "#":
                continue
            elif command == "1":
                self.add_entry()
            elif command == "2":
                self.choose_date()
            elif command == "3":
                self.manage_variables()
            else:
                self.export()





interface = Interface()
interface.execute()




    




