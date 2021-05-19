""" test script which finds new usb devices then connects to them.

run the script without the new device connected. When prompted 
connect the device and press enter at the cursor.

The script will attempt to connect ot the first new usb device found.

You can make the output less verbose by setting VERBOSE = False
"""
VERBOSE = False

import usb

def find_usbs() -> list:
    usb_list = usb.core.find(find_all=True)
    ids_list = []
    for id, device in enumerate(usb_list):
        if VERBOSE: print(f"Vendor ID: {device.idVendor} Product ID: {device.idProduct}")
        ids_list.append((device.idVendor,device.idProduct))

    if VERBOSE: print(f'Total devices: {len(ids_list)}')
    return ids_list

def find_new_usb() -> list:
    pre_usbs = find_usbs()
    input("connect new usb device then press return: ")
    post_usbs = find_usbs()

    if not len(post_usbs) > len(pre_usbs):
        print("no new devices found")
        return None
    else:
        new_usbs = [usb for usb in post_usbs if usb not in pre_usbs]
        if VERBOSE:
            for device in new_usbs:
                print("The following new devices were found:")
                print(f"\tVendor ID: {device[0]} Product ID: {device[1]}")       
        return new_usbs

def connect_usb(ids: tuple):
    vendor_id, product_id = ids
    connection = usb.core.find(vendor_id, product_id)
    if connection:
        print(f"connected to Vendor ID: {vendor_id} Product ID: {product_id}")
        return connection
    
    print("failed to connect")
    


if __name__ == "__main__":
    new_usb_ids = find_new_usb() # note returns a list
    if new_usb_ids:
        new_usb_id = new_usb_ids[0]
        timy = connect_usb(new_usb_id) #connect to first new usb in list

        # now lets see what configurations the timy has
        for cfg in timy:
            print(str(cfg.bConfigurationValue))
