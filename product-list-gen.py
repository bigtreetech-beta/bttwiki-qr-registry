import json
import os

def load_template(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_product_list(dir_path):
    product_list = []
    for filename in os.listdir(dir_path):
        if filename.endswith(".json"):
            file_path = os.path.join(dir_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    product_list.append(data)
                else:
                    print(f"skip file {filename} is not valid config")
    return product_list

def replace_marker(obj, product_list, marker):
    if isinstance(obj, list):
        new_list = []
        for item in obj:
            if item == marker:
                new_list.extend(product_list)
            else:
                new_list.append(replace_marker(item, product_list, marker))
        return new_list
    elif isinstance(obj, dict):
        return {k: replace_marker(v, product_list, marker) for k, v in obj.items()}
    else:
        return obj

def check_filepath(file_path:str):
    if not os.path.exists(file_path):
        os.makedirs(file_path)

def save_result(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # config 
    template_file_path = "template-file/config-template.json"
    product_base_dir = "product-base"
    build_dir = ".build"
    output_file_path = f"{build_dir}/product-list.json"
    insert_mark = "<--- product insert --->"

    check_filepath(f"{build_dir}")

    template_data = load_template(template_file_path)
    product_list = load_product_list(product_base_dir)
    result_data = replace_marker(template_data, product_list, insert_mark)
    save_result(result_data, output_file_path)
    print(f"file at -> {output_file_path}")
