import qrcode
import json
import os

def qrcode_gen(uuid, url_base, build_dir, size:int=1200):
    prod_url = f"{url_base}/?uuid={uuid}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(prod_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((size, size))

    img.save(f"{build_dir}/qrcode/{uuid}.png")

def check_filepath(file_path:str):
    if not os.path.exists(file_path):
        os.makedirs(file_path)

def read_uuid_json(config_file:str):
    uuid_data = []
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            product_list = data.get("product_list", [])

            if isinstance(product_list, list):
                for item in product_list:
                    uuid = item.get("uuid")
                    uuid_data.append(str(uuid))
            else:
                print("productlist error")

    except FileNotFoundError:
        print(f"file in {config_file} not found")
    except json.JSONDecodeError:
        print(f"file in {config_file} not valid json file")
    
    return uuid_data

def read_config_url(config_file:str):
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            config_url = data.get("config_url")

    except FileNotFoundError:
        print(f"file in {config_file} not found")
    except json.JSONDecodeError:
        print(f"file in {config_file} not valid json file")

    return config_url

if __name__ == "__main__":
    product_file = ".build/product-list.json"
    build_dir = ".build"
    qrcode_size:int = 1200

    check_filepath(f"{build_dir}/qrcode")

    config_url = read_config_url(product_file)
    uuid_list = read_uuid_json(product_file)

    print(f"{config_url} {uuid_list}")
    for uuid in uuid_list:
        print(f"generate {uuid}")
        qrcode_gen(uuid, config_url, build_dir, qrcode_size)

    print("done")
