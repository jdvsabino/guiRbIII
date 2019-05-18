def atom_number(im):

    return im.atom_num
    

def sigma_H(im):

    if len(im.abs_pic.fit_pars["x"])  == 0:
        return -1
    
    return im.abs_pic.fit_pars["x"][2]


def sigma_V(im):
    
    if len(im.abs_pic.fit_pars["y"])  == 0:
        return -1
    
    return im.abs_pic.fit_pars["y"][2]


def gen_func_dict(var, func):

    func_dict = dict()
    
    for i in range(len(var)):
        func_dict[var[i]] = func_list[i]

    return func_dict

var_list  = ["Atom Number", "Sigma H", "Sigma V"]
func_list = [atom_number, sigma_H, sigma_V]

func_dict = gen_func_dict(var_list, func_list)

