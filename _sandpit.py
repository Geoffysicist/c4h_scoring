import yaml
import c4h_score as c4h

fn = "test.c4ha"
articles = []
articles.append(c4h.C4HArticle(100))
articles.append(c4h.C4HArticle(200))
with open(fn, 'w') as out_file:
    out_file.write('--- # C4H Articles\n')
    yaml.dump(self, out_file)


# class test_class(object):
#     def __init__(self):
#         self.att1 = 1
#         self.att2 = 'two'

# test_instance = test_class()
# print(test_instance.att2)
# setattr(test_instance, 'att2', 2)
# print(test_instance.att2)
# setattr(test_instance, 'att3', 3)
# print(test_instance.att3)
# setattr(x, 'y', v) is equivalent to x.y = v


# string = "two_word string"
# split_string = string.split(" ")
# join_string = " ".join(split_string[1:])
# print(join_string)
# string = "three word string"
# split_string = string.split(" ")
# join_string = " ".join(split_string[1:])
# print(join_string)

# this_list = ['a', 'b', 3, 100]

# for i, val in enumerate(this_list, 2):
#     print(i)