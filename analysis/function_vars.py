def atom_number(im):

    return im.atom_num
    

def sigma_H(im):

    print("This is sigma_H! :D")
    return 1


def sigma_V(im):

    print("This is sigma_V! :D")
    return 0


def gen_func_dict(var, func):

    func_dict = dict()
    
    for i in range(len(var)):
        func_dict[var[i]] = func_list[i]

    return func_dict

var_list = ["Atom Number", "Sigma H", "Sigma V"]
func_list = [atom_number, sigma_H, sigma_V]

func_dict = gen_func_dict(var_list, func_list)

