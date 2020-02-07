"""
Test the output of fill_completions()
-------------------------------------

>>> c_dict = fill_completions('articles.txt')

Find words with 'e', 'a' and 't' at indices 1, 2, and 3:

>>> eat_words = {'beaten', 'death', 'deaths', 'deaton', 'feather', 'feathers', 'feature', 'featured', 'features',
... 'featuring', 'heat', 'heath', 'heather', 'heating', 'heaton', 'meat', 'neat', 'seat', 'seattle', 'weather',
... 'weathered', 'weathermen'}

>>> eat_words.issubset(c_dict[(1,'e')] & c_dict[(2,'a')] & c_dict[(3, 't')])
True

>>> ea_t_words = {'earth', 'east', 'easter', 'eastern', 'easton'}

>>> ea_t_words.issubset(c_dict[(0, 'e')] & c_dict[(1, 'a')] & c_dict[(3, 't')])
True


Test the output of find_completions()
-------------------------------------

>>> geo_words = {'geoffrey', 'geographical', 'george', 'georgia'}

>>> geo_words.issubset(find_completions('geo', c_dict))
True

>>> eat_words = {'eat'}
>>> eat_words.issubset(find_completions('eat', c_dict))
True
"""
import re
filename = 'articles.txt'
def fill_completions(filename):
    result = {}
    lines = open(filename,"rb").read().split()
    dictionary = "abcdefghijklmnopqrstuvwxyz"
    for word in lines:
        # change byte to string, strip the special character and
        # skip case that length is one or not string.
        word = word.decode("utf-8")
        word = re.sub(r'[^\w\s]','', word)
        word = word.lower()
        if type(word) is not str:
            continue
        if len(word) <= 1:
            continue
        if len(word) > 1:
            count = 0
            for char in word:
                # if the pair exist, add the word, if not, create new key.
                if char in dictionary:
                    if (count,char) not in result.keys():
                        result[(count,char)] = set([word])
                        count += 1
                    else:
                        result[(count, char)].add(word)
                        count += 1
    return result


def find_completions(prefix, c_dict):
    result = []
    temp = set(c_dict[(0,prefix[0])])
    for count,char in enumerate(prefix):
        if char == ' ':
            continue
        # take intersection for values in dictionary one by one
        temp1 = c_dict[(count,char)]
        temp = (temp.intersection(set(temp1)))
        final = list(temp)

    return final

def main():
    c_dict = (fill_completions(filename))

    while True:
        prefix = input('Enter a prefix:')
        result = find_completions(prefix, c_dict)
        if prefix == 'quit':
            exit()
        elif len(result) < 1:
            print("No completions")
            exit()
        else:
            print(sorted(result))

    return None


if __name__ == '__main__':
    main()

