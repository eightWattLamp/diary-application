def clear(word: str):

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
    
def input_command(message: str, options: tuple):
        while True:
            response = input(message)

            if response == "#":
                return response

            if not response in options:
                print("invalid input")

                expected = ""

                for option in options:
                    expected += option + ", "
                
                expected = expected[0: len(expected) - 2] # remove the comma and the space at the end

                print("expected input: ", expected)
                print()
                continue

            print()
            return response
    
def input_name(message: str):
        while True:
            response = clear(input(message))

            if response == "#":
                return response

            if response == "":
                print("invalid input, special characters are not allowed")
                print()
                continue
            
            break

        print()
        return response
    
def input_num(message: str, int_expected = True):
        while True:
            response = input(message)

            if int_expected:
                try:
                    if response == "#":
                        return response
                    response = int(response)
                    break
                except:
                    print("invalid input, a whole number is expected")
                    print()
            else:
                try:
                    if response == "#":
                        return response
                    response = float(response)
                    break
                except:
                    print("invalid input, a number is expected")
                    print()
        
        print()
        return response   