import os








if __name__ == "__main__":
    file_path = "/data//ekg_data/01.Ruhe.txt"

    file_type = detect_file_type(file_path)

    if file_type == ".json":
        print("This is a JSON file.")
    elif file_type == ".csv":
        print("This is a CSV file.")
    elif file_type == ".fit":
        print("This is a FIT file.")
    elif file_type == ".txt":
        print("This is a text file.")
    else:
        print("Unknown file type.")