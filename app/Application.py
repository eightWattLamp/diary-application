import os
from datetime import datetime, timedelta
import uuid
import scripts.input_utils as ut

class FileManager:

    def __init__(self):
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



    def is_date_recorded(self, date_str: str):
        found = False
        with open(self.__days_dir, "r") as day_file:
            for line in day_file:
                try:
                    if line.split(",")[1].strip() == date_str:
                        found = True
                except:
                    break

        return found 

    def add_entry(self, entry: dict, date_str: str):    
        cur_id = uuid.uuid4()
        
        with open(self.__days_dir, "a") as day_file:
            day_file.write(str(cur_id) + "," + date_str + "\n")
        
        for variable in entry:
            with open(self.find_variable(variable), "a") as var_file:
                var_file.write(str(cur_id) + "," + str(entry[variable]) + "\n")



    def export(self, name):
        filename = name + ".csv"
        file_dir = os.path.join(self.__export_dir, filename)
        with open(self.get_days_file(), "r") as day_file, open(file_dir, "a") as export_file:

            head = "date"
            variables = self.get_variables()
            for variable in variables:
                head += "," + variable
            head += "\n"
            export_file.write(head)


            next(day_file) # skipping the head
            for day in day_file:
                day_id = day.strip().split(",")[0]
                day_str = day.strip().split(",")[1]
                new_line = day_str
                for variable in variables:
                    var_dir = self.find_variable(variable)
                    with open(var_dir, "r") as var_file:
                        next(var_file) # skipping the head
                        for line in var_file:
                            var_id = line.strip().split(",")[0]
                            if var_id == day_id:
                                var_val = line.strip().split(",")[1]
                                new_line += "," + var_val # adding the value of the variable corresponding to the date
                                break
                        else:
                            new_line += "," + "NA" # missing value if nothing found
                
                new_line += "\n"
                export_file.write(new_line)



class Interface:
    def __init__(self):
        self.__manager = FileManager()
        self.__cur_date = datetime.today()
        self.__date_format = "%d.%m.%Y"
    


    def print_variables(self):

        active = self.__manager.get_variables(True)
        inactive = self.__manager.get_variables(False)

        print("ACTIVE:")
        print()

        if len(active) == 0:
            print("None")
        else:
            for var in active:
                print(var)
        
        print()

        print("INACTIVE:")
        print()

        if len(inactive) == 0:
            print("None")
        else:
            for var in inactive:
                print(var)
        
        print()

        pass

    def update_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        os.system('cls' if os.name == 'nt' else 'clear')

        weekdays = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
        weekday = weekdays[self.__cur_date.weekday()]

        date_str = weekday + " - " + self.__cur_date.strftime("%d.%m.%Y")

        print("# - Main menu")

        print(len(date_str) * "=")
        print(date_str)
        print(len(date_str) * "=")



    def add_variable(self):
        name = self.search_variable("new", "name of a new variable: ")
        var_type = ut.input_command("type of a new variable (1 - Numeric, 2 - Categorical): ", ("1", "2"))

        if var_type == "#":
            return var_type

        categories = []

        if var_type == "2":
            category_num = ut.input_num("number of categories: ")

            if category_num == "#":
                return category_num

            for i in range(0, category_num):
                category = ut.input_name(f"category {i + 1}: ")

                if category == "#":
                    return category

                categories.append(category)
        
        self.__manager.add_variable(name, categories)

    def search_variable(self, type = "existing", message = "name: "):
        while True:
            name = ut.input_name(message)

            if name == "#":
                return name

            if type == "existing":
                if self.__manager.find_variable(name) == None:
                    print("variable not found")
                    print()
                else:
                    return name
            else:
                if self.__manager.find_variable(name) == None:
                    return name
                else:
                    print("variable with this name already exists")
                    print()

    def move_variable(self):
        name = self.search_variable("existing")
        self.__manager.move_variable(name)
    
    def rename_variable(self):
        cur_name = self.search_variable("existing", "current name: ")
        new_name = self.search_variable("new", "new name: ")
        if new_name == "#":
            return new_name
        self.__manager.rename_variable(cur_name, new_name)

    def delete_variable(self):
        name = self.search_variable("existing", "variable to delete: ")
        count = self.__manager.check_variable(name)
        if count == 0:
            warn = ""
        elif count == ">100":
            warn = "more than 100"
        else:
            warn = str(count)
        if warn != "":
            confirm = ut.input_command(f"The variable {name} has {warn} entries, are you sure you want to delete it? 1 - yes, delete {name}, 0 - no, keep {name}: ", ("1", "0"))
            if confirm == "0" or confirm == "#":
                return
        self.__manager.delete_variable(name)
        
    def manage_variables(self):
        while True:
            self.update_screen()
            self.print_variables()
            command = ut.input_command("1 - Add a variable, 2 - (in)activate a variable, 3 - Rename a variable, 4 - Delete a variable: ", ("1", "2", "3", "4"))
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



    def add_entry(self):

        active_variables = self.__manager.get_variables()

        if len(active_variables) == 0:
            print("no active variables")
            input("press enter to continue")
            return
        
        cur_date_str = self.__cur_date.strftime(self.__date_format)
        
        if self.__manager.is_date_recorded(cur_date_str):
            print("an entry for this date already exists")
            input("press enter to continue")
            return

        entry = {}

        message = "adding an entry for variables "
        for variable in active_variables:
            message += variable + ", "
        message = message[0:len(message)-2]
        message += ":"
        
        print(message)
        print()

        for variable in active_variables:
            options = self.__manager.get_options(variable)

            if len(options) == 0:
                inp = ut.input_num(variable + ": ", int_expected=False)

                if inp == "#":
                    return inp

                entry[variable] = inp
            else:
                inp = ut.input_command(variable + ": ", options)

                if inp == "#":
                    return inp

                entry[variable] = inp

        self.__manager.add_entry(entry, cur_date_str)
        
        self.__cur_date = self.__cur_date + timedelta(days=1)
        
    def choose_date(self):
        while True:
            date_str = input("date: ")

            if date_str == "#":
                return date_str

            try:
                date = datetime.strptime(date_str, self.__date_format)
            except:
                print("invalid input, enter the date in the following format: dd.mm.yyyy")
                print()
                continue

            break

        if date == "#":
            return date

        self.__cur_date = date

    def export(self):
        name = ut.input_name("name of the export file: ")
        self.__manager.export(name)
        print("the data was exported as a " + name + ".csv" + " file")
        input("press enter to continue")

    def execute(self):
        while True:

            self.update_screen()

            command = ut.input_command("1 - Add an entry, 2 - Choose date, 3 - Manage variables, 4 - Export data: ", ("1", "2", "3", "4"))

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




    




