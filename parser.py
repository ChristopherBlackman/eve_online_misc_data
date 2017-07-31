import pprint
import yaml
import csv
from yaml import load, dump

# eve sde realative path, resource here :
# https://developers.eveonline.com/resource/resources
path = "sde/fsd/blueprints.yaml"

pp = pprint.PrettyPrinter(indent=4)

def main():
    stream = None
    data = None
    normalized_data_list = []

    # gets data from the eve sde
    try:
        stream = file(path, "r")
        data = yaml.load(stream)
    finally:
        stream.close()

    
    # normalizes data
    for item in data:         
        normal_data = decode_data(data[item],item)
        if normal_data is not None:
           normalized_data_list.append(normal_data) 

    # export data
    write_to_csv(normalized_data_list)


'''
    input : normal_data_list
    expected-format : {'bpo_id':bpo_id, 'materials_list':_materials_list,'product_id':_product_id,'product_quantity':_product_quantity}
    output : None
    description : writes data to file in csv format
    return : None
'''
 
def write_to_csv(normal_data_list):
    f = None
    fieldnames = ['bpo_id','activityID', 'material_id', 'materials_quantity','product_id','product_quantity']

    try:
        csvfile = file("data.csv", "w")
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in normal_data_list:
            for material in item['materials_list']:
                writer.writerow(\
                        {'bpo_id': item['bpo_id'],\
                            'activityID': 1,\
                            'material_id': material['typeID'],\
                            'materials_quantity': material['quantity'],\
                            'product_id':item['product_id'],\
                            'product_quantity': item['product_quantity']})

    finally:
        csvfile.close()


'''
    input : data
        data-description : python object data of parsed yaml
    input : bpo_id
    output : None
    description : gets useful data out of yaml represented object
    return : normalized data
        return-format : {'bpo_id':bpo_id, 'materials_list':_materials_list,'product_id':_product_id,'product_quantity':_product_quantity}
'''
def decode_data(data,bpo_id):

    try:
        _materials_list = data['activities']['manufacturing']['materials']
        _product_id = data['activities']['manufacturing']['products'][0]['typeID']
        _product_quantity= data['activities']['manufacturing']['products'][0]['quantity']
    except KeyError:
        return None

    return {'bpo_id':bpo_id, 'materials_list':_materials_list,'product_id':_product_id,'product_quantity':_product_quantity}



main()
