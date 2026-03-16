# Function to print dictionary values given the keys
def print_values_of(dictionary, keys):
    for key in keys:
        print(dictionary[key]) # Changed k to key.


# Print dictionary values from simpson_catch_phrases
simpson_catch_phrases = {"lisa": "BAAAAAART!", 
                         "bart": "Eat My Shorts!", 
                         "marge": "Mmm~mmmmm", 
                         "homer": "d'oh!",  # Changing the speech marks to have the full string within them.
                         "maggie": "(Pacifier Suck)"
                         }


print_values_of(simpson_catch_phrases, ["lisa", "bart", "homer"]) # This should only have two arguments.
# Used dictionary name as argument 1 and a list of the needed keys as argument 2.

'''
    Expected console output:

    BAAAAAART!
    Eat My Shorts!
    d'oh!

'''
