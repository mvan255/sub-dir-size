from collections import namedtuple

global leaf_list

Leaf = namedtuple("leaf", "strpath path size")



def get_all_children(path, leafs):
    def asdf(): # helper generator
        for leaf in leafs:
            if (
                    len(leaf.path) > len(path) # make sure we can zip these lists
                    and 
                    all(
                        # the beginning of leaf.path is identical to path 
                        a == b for (a, b) in zip(path, leaf.path[:len(path)])
                    )
                ):
                yield leaf
    return list(asdf())



def cumulative_size(path, leafs):
    all_children = get_all_children(path, leafs)
    if len(all_children) == 0:
        # path is a leaf, so find it in the leaf list
        all_children = filter(
                # leaf path matches exactly
                lambda x: len(x.path) == len(path) and all( a == b for (a,b) in zip(path, x.path) ),
                leafs
            )
    # return the cumulative size in gigabytes
    return float(sum(x.size for x in all_children)) / float(10**6)


def str_path_to_path_list(str_path):
    return str_path.split("/")

def get_leafs_list(iter_leaf_data): # I know it's leaves not leafs but I think leafs is funny
    def asdf(): # helper generator
        for leaf in iter_leaf_data:
            (path, size) = leaf.split(" ---- ")
            size = int(size) if int(size) else 1 # if size is 0KB round up to 1KB
            yield Leaf(strpath=path, path=str_path_to_path_list(path), size=size) 
    return list(asdf())

def list_dir(path, leafs):
    children = get_all_children(path, leafs)
    
    # create a set of the items in this directory
    immediate_children = set( x.path[len(path)] for x in children )

    # get each item's size
    sizes = [(child, cumulative_size(path + [child], children)) for child in immediate_children]
    # sort: largest item first
    sizes.sort(reverse=True, key=lambda x: x[1])

    for child, s in sizes:
        print(f'"{child}", {round(s, 3)}')



# can quickly update leaf_list after saving the data file by calling this
def doit():
    global leaf_list
    with open("filesizes.txt") as infofile:
        leaf_list = get_leafs_list(infofile)


# shorthand for list_dir function call
#       only have to type "q(<path>)" instead of 
#       "list_dir(str_path_to_path_list(<path>), leaf_list)"
q = lambda qq: list_dir(str_path_to_path_list(qq), leaf_list)

if __name__ == "__main__":
    doit()
