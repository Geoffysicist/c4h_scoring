import design_helpers as dh

comp_list = [complex(0,0), complex(0,1), complex(1,1), complex(1,0)]

print(dh.bezier(comp_list, 8))
print(dh._bezier(comp_list, 8))